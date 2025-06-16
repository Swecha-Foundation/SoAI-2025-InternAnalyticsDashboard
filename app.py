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

# --- UNIFIED SESSION STATE & DATA LOADING ---

@st.cache_data
def load_all_data():
    """Fetches both datasets and returns them as a tuple."""
    ai_data = fetch_data(API_URL, HEADERS)
    techlead_data = fetch_data(LEAD_URL, HEADERS)
    return ai_data, techlead_data

# Load the data once using the cached function
ai_data, techlead_data = load_all_data()

# Initialize session state
if "intern_type" not in st.session_state: st.session_state.intern_type = "ai"
if "data" not in st.session_state: st.session_state.data = None
if "cohort_type" not in st.session_state: st.session_state.cohort_type = "cohort1"
if "view_type" not in st.session_state: st.session_state.view_type = "tabular"

# --- UI CONTROLS ---

st.subheader("Select Cohort")
selected_cohort = st.selectbox("Choose a cohort:", ["cohort1", "cohort2"], key="cohort_selector")
st.session_state.cohort_type = selected_cohort
st.subheader(f"Selected Cohort: {st.session_state.cohort_type.upper()}")

st.subheader("Select View Type")
selected_view = st.selectbox(
    "Choose a view type:",
    ["tabular", "sankey", "sunburst"],
    format_func=lambda x: {"tabular": "Tabular View", "sankey": "Sankey Diagram View", "sunburst": "Sunburst View"}[x],
    key="view_selector"
)
st.session_state.view_type = selected_view

# Refresh button to manually clear cache and re-fetch data
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# --- DISPLAY CONTENT BASED ON VIEW TYPE ---

if ai_data is not None and techlead_data is not None:
    if st.session_state.view_type == "tabular":
        st.subheader("Select Intern Type for Tabular View")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤖 AI Developer Intern", use_container_width=True):
                st.session_state.intern_type = "ai"
                st.session_state.data = ai_data
        with col2:
            if st.button("🧑‍💻 Tech Lead Intern", use_container_width=True):
                st.session_state.intern_type = "techlead"
                st.session_state.data = techlead_data

        if st.session_state.data is not None:
            display_data(st.session_state.data, st.session_state.cohort_type, st.session_state.intern_type)
        else:
            st.info("Please select an intern type to load the Tabular View.")

    elif st.session_state.view_type == "sankey":
        # The data is already loaded, so we just pass it.
        display_sankey_diagram(ai_data, techlead_data, st.session_state.cohort_type)

    elif st.session_state.view_type == "sunburst":
        display_sunburst_diagram(ai_data, techlead_data, st.session_state.cohort_type)
else:
    st.error("Could not fetch the required data. Please check your API connection and secrets, then click the Refresh button.")