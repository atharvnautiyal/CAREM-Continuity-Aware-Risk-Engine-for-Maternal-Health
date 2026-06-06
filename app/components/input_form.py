import streamlit as st


def render_input_form():
    st.markdown("## 📝 Patient Information")

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("Patient Name", key="patient_name")
        age = st.number_input("Age", 10, 60, 25, key="age")
        systolic_bp = st.number_input("Systolic BP", 70, 200, 120, key="systolic_bp")
        bs = st.number_input("Blood Sugar", 4.0, 20.0, 7.0, key="blood_sugar")

    with col2:
        patient_id = st.text_input("Patient ID", key="patient_id")
        diastolic_bp = st.number_input("Diastolic BP", 40, 130, 80, key="diastolic_bp")
        body_temp = st.number_input("Body Temperature (F)", 95.0, 105.0, 98.6, key="body_temp")
        heart_rate = st.number_input("Heart Rate", 40, 150, 80, key="heart_rate")

    st.markdown("---")

    return {
        "PatientName": patient_name,
        "PatientID": patient_id,
        "Age": age,
        "SystolicBP": systolic_bp,
        "DiastolicBP": diastolic_bp,
        "BS": bs,
        "BodyTemp": body_temp,
        "HeartRate": heart_rate
    }