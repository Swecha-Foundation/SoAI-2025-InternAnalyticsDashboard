import streamlit as st
from data import fetch_data
from script import display_data

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

# Buttons for cohort selection
col1, col2 = st.columns(2)
with col1:
    if st.button("COHORT 1"):
        st.session_state.cohort_type = "cohort1"
        st.session_state.intern_type = None  # Reset intern type

with col2:
    if st.button("COHORT 2"):
        st.session_state.cohort_type = "cohort2"
        st.session_state.intern_type = None  # Reset intern type

# If a cohort is selected
if st.session_state.cohort_type:
    st.subheader(f"Selected Cohort: {st.session_state.cohort_type.upper()}")

    # Buttons for intern types
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
else:
    st.info("Please select a cohort type.")
