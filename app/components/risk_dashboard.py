import streamlit as st

def show_result(result: dict, patient_data: dict):
    st.title("Risk Assessment Dashboard")

    risk = result.get("risk_level", "Unknown")
    recommendation = result.get("recommendation", "No recommendation available.")
    confidence = result.get("confidence", 0)
    probabilities = result.get("class_probabilities", {})
    continuity = result.get("continuity", {})

    st.markdown("## 🩺 Patient Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Age", patient_data.get("Age", "N/A"))
    col2.metric("Systolic BP", patient_data.get("SystolicBP", "N/A"))
    col3.metric("Diastolic BP", patient_data.get("DiastolicBP", "N/A"))

    col1, col2, col3 = st.columns(3)
    col1.metric("Blood Sugar", patient_data.get("BS", "N/A"))
    col2.metric("Body Temp", patient_data.get("BodyTemp", "N/A"))
    col3.metric("Heart Rate", patient_data.get("HeartRate", "N/A"))

    st.markdown("---")

    st.markdown("## 🧾 Risk Overview")

    if risk.lower() == "low risk":
        st.markdown(
            "<div style='padding:20px; border-radius:10px; background-color:#dcfce7; color:#166534;'>"
            f"<h3>🟢 {risk}</h3></div>",
            unsafe_allow_html=True
        )
    elif risk.lower() == "mid risk":
        st.markdown(
            "<div style='padding:20px; border-radius:10px; background-color:#fef9c3; color:#854d0e;'>"
            f"<h3>🟡 {risk}</h3></div>",
            unsafe_allow_html=True
        )
    elif risk.lower() == "high risk":
        st.markdown(
            "<div style='padding:20px; border-radius:10px; background-color:#fee2e2; color:#991b1b;'>"
            f"<h3>🔴 {risk}</h3></div>",
            unsafe_allow_html=True
        )
    else:
        st.info(risk)

    st.metric("Prediction Confidence", f"{confidence * 100:.2f}%")

    st.markdown("---")

    st.markdown("## 📈 Risk Probabilities")
    st.markdown("### Risk Distribution")

    col1, col2, col3 = st.columns(3)
    labels = ["low risk", "mid risk", "high risk"]
    cols = [col1, col2, col3]

    for i, label in enumerate(labels):
        if label in probabilities:
            prob = probabilities[label] * 100
            cols[i].metric(label.title(), f"{prob:.1f}%")

    st.markdown("---")

    st.markdown("## 🔄 Continuity Analysis")

    if continuity:
        trend_status = continuity.get("trend_status", "Unknown")
        continuity_score = continuity.get("continuity_score", "N/A")
        continuity_alert = continuity.get("alert", "No alert available.")
        reasons = continuity.get("reasons", [])
    else:
        trend_status = "No trend data available"
        continuity_score = "N/A"
        continuity_alert = "Continuity analysis is not available yet."
        reasons = []

    if trend_status == "critical worsening":
        st.error(f"Trend Status: {trend_status.title()}")
    elif trend_status == "worsening":
        st.warning(f"Trend Status: {trend_status.title()}")
    elif trend_status == "improving":
        st.success(f"Trend Status: {trend_status.title()}")
    else:
        st.info(f"Trend Status: {trend_status.title()}")

    st.write(f"**Continuity Score:** {continuity_score}")
    st.write(f"**Alert:** {continuity_alert}")

    if reasons:
        st.markdown("### Reasons")
        for reason in reasons:
            st.write(f"- {reason}")

    st.markdown("---")

    st.markdown("### 🧠 Clinical Recommendation")

    if risk.lower() == "high risk":
        st.error(recommendation)
    elif risk.lower() == "mid risk":
        st.warning(recommendation)
    else:
        st.success(recommendation)

    st.markdown("---")

    st.markdown("## 📊 Basic Insights")

    insights = []

    if patient_data.get("SystolicBP", 0) >= 140:
        insights.append("High systolic blood pressure detected.")

    if patient_data.get("DiastolicBP", 0) >= 90:
        insights.append("High diastolic blood pressure detected.")

    if patient_data.get("BS", 0) >= 11:
        insights.append("Elevated blood sugar level.")

    if patient_data.get("BodyTemp", 0) >= 100:
        insights.append("High body temperature detected.")

    if patient_data.get("HeartRate", 0) >= 100:
        insights.append("Elevated heart rate detected.")

    if insights:
        for insight in insights:
            st.warning(insight)
    else:
        if risk.lower() == "high risk":
            st.warning("Vitals appear normal individually, but combined factors indicate elevated risk.")
        else:
            st.success("All vitals are within normal range.")