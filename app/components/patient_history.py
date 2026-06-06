import streamlit as st
import pandas as pd
from database.queries import get_all_records, get_records_by_patient_id


def show_patient_history():
    st.title("Patient History Records")

    records = get_all_records()

    if not records:
        st.info("No patient records available yet.")
        return

    df = pd.DataFrame(records, columns=[
        "Patient Name",
        "Patient ID",
        "Age",
        "Systolic BP",
        "Diastolic BP",
        "Blood Sugar",
        "Body Temp",
        "Heart Rate",
        "Risk Level",
        "Recommendation",
        "Created At"
    ])

    st.metric("Total Records", len(df))

    patient_ids = ["All"] + sorted(df["Patient ID"].astype(str).unique().tolist())
    selected_id = st.selectbox(
        "Filter by Patient ID",
        patient_ids,
        key="patient_history_filter"
    )

    if selected_id != "All":
        df = df[df["Patient ID"].astype(str) == selected_id]

    st.subheader("Saved Records")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Records as CSV",
        data=csv,
        file_name="patient_history.csv",
        mime="text/csv",
        key="download_patient_history_csv"
    )

    if selected_id != "All":
        st.markdown("---")
        st.subheader("Patient Trend Analysis")

        patient_records = get_records_by_patient_id(selected_id)

        if not patient_records:
            st.info("No trend data available for this patient.")
            return

        patient_df = pd.DataFrame(patient_records, columns=[
            "Patient Name",
            "Patient ID",
            "Age",
            "Systolic BP",
            "Diastolic BP",
            "Blood Sugar",
            "Body Temp",
            "Heart Rate",
            "Risk Level",
            "Recommendation",
            "Created At"
        ])

        patient_df["Created At"] = pd.to_datetime(patient_df["Created At"])
        patient_df = patient_df.sort_values("Created At")

        st.write(f"Showing trend analysis for Patient ID: **{selected_id}**")

        st.line_chart(
            patient_df.set_index("Created At")[["Systolic BP", "Diastolic BP"]]
        )

        st.line_chart(
            patient_df.set_index("Created At")[["Blood Sugar"]]
        )

        st.line_chart(
            patient_df.set_index("Created At")[["Heart Rate"]]
        )

        risk_map = {
            "low risk": 1,
            "mid risk": 2,
            "high risk": 3
        }

        patient_df["Risk Score"] = patient_df["Risk Level"].str.lower().map(risk_map)

        st.line_chart(
            patient_df.set_index("Created At")[["Risk Score"]]
        )

        st.caption("Risk Score Mapping: Low Risk = 1, Mid Risk = 2, High Risk = 3")