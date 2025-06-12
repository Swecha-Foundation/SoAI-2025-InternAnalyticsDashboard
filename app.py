import streamlit as st
from data import fetch_data
from script import display_data, display_sankey_diagram, display_sunburst_diagram

# Secrets from .streamlit/secrets.toml
API_TOKEN = st.secrets["API_TOKEN"]
API_URL = st.secrets["API_URL"]
LEAD_URL = st.secrets["LEAD_URL"]

HEADERS = {
    "accept": "application/json",
    "xc-token": API_TOKEN
}

# Streamlit App Setup
st.set_page_config(page_title="Intern Registrations Dashboard", layout="wide")
st.title("🎓 Intern Registrations Dashboard")

# Initialize session state
if "intern_type" not in st.session_state:
    st.session_state.intern_type = "ai"
if "data" not in st.session_state:
    st.session_state.data = None
if "cohort_type" not in st.session_state:
    st.session_state.cohort_type = "cohort1"  # Default to cohort1
if "view_type" not in st.session_state:
    st.session_state.view_type = "tabular"  # Default to tabular view

# Cohort selection dropdown
st.subheader("Select Cohort")
cohort_options = ["cohort1", "cohort2"]
selected_cohort = st.selectbox(
    "Choose a cohort:",
    cohort_options,
    index=cohort_options.index(st.session_state.cohort_type),
    key="cohort_selectbox"
)

# Update session state if cohort changes
if selected_cohort != st.session_state.cohort_type:
    st.session_state.cohort_type = selected_cohort

# If a cohort is selected
if st.session_state.cohort_type:
    st.subheader(f"Selected Cohort: {st.session_state.cohort_type.upper()}")

    st.subheader("Select View Type")
    view_options = ["tabular", "sankey", "sunburst"]
    view_labels = ["Tabular View", "Sankey Diagram View", "Sunburst View"]
    selected_view = st.selectbox(
        "Choose a view type:",
        view_options,
        format_func=lambda x: view_labels[view_options.index(x)],
        index=view_options.index(st.session_state.view_type),
        key="view_selectbox"
    )

    # Update session state if view type changes
    if selected_view != st.session_state.view_type:
        st.session_state.view_type = selected_view

    # Buttons for intern types
    if st.session_state.view_type == "tabular":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤖 AI Developer Intern"):
                st.session_state.intern_type = "ai"
                with st.spinner("Fetching AI Developer Intern data..."):
                    st.session_state.data = fetch_data(API_URL, HEADERS)

        with col2:
            if st.button("🧑‍💻 Tech Lead Intern"):
                st.session_state.intern_type = "techlead"
                with st.spinner("Fetching Tech Lead Intern data..."):
                    st.session_state.data = fetch_data(LEAD_URL, HEADERS)

        # Refresh button
        if st.button("🔄 Refresh"):
            fetch_data.clear()
            if st.session_state.intern_type:
                with st.spinner("Refreshing data..."):
                    if st.session_state.intern_type == "techlead":
                        st.session_state.data = fetch_data(LEAD_URL, HEADERS)
                    else:
                        st.session_state.data = fetch_data(API_URL, HEADERS)

        # Display data
        if st.session_state.data is not None:
            display_data(st.session_state.data, st.session_state.cohort_type, st.session_state.intern_type)
        else:
            st.info("Please select an intern type to load data.")
    elif st.session_state.view_type == "sankey":
        display_sankey_diagram()
    elif st.session_state.view_type == "sunburst":
        display_sunburst_diagram()
else:
    st.info("Please select a cohort type.")
