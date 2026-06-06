import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.components.input_form import render_input_form
from app.components.risk_dashboard import show_result
from app.components.patient_history import show_patient_history
from backend.services.data_validator import validate_input
from backend.services.risk_calculator import calculate_risk
from database.queries import create_table, insert_record

st.set_page_config(
    page_title="CAREM",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1, h2, h3 {
    color: #1f2937;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1em;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #1d4ed8;
    color: white;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

create_table()

st.title("CAREM: Maternal Risk Prediction System")

page = st.sidebar.selectbox(
    "Select Page",
    ["New Prediction", "Patient History"],
    key="main_navigation"
)

if page == "New Prediction":
    left, center, right = st.columns([1, 2, 1])

    with center:
        patient_data = render_input_form()

        if st.button("Predict Risk", key="predict_risk_button"):
            errors = validate_input(patient_data)

            if errors:
                for error in errors:
                    st.error(error)
            else:
                result = calculate_risk(patient_data)
                insert_record(patient_data, result)
                show_result(result, patient_data)
                st.success("✅ Patient record saved to database")

elif page == "Patient History":
    show_patient_history()