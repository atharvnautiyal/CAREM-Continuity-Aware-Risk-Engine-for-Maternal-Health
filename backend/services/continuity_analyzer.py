from database.queries import get_records_by_patient_id

def analyze_continuity(patient_data: dict):
    patient_id = patient_data["PatientID"]
    past_records = get_records_by_patient_id(patient_id, limit=3)

    if not past_records:
        return {
            "trend_status": "new patient",
            "alert": "No past records found. Continuity analysis not available.",
            "continuity_score": 0,
            "reasons": []
        }

    worsening_points = 0
    improving_points = 0
    reasons = []

    latest_systolic = patient_data["SystolicBP"]
    latest_diastolic = patient_data["DiastolicBP"]
    latest_bs = patient_data["BS"]
    latest_hr = patient_data["HeartRate"]

    systolic_values = [row[3] for row in past_records if row[3] is not None]
    diastolic_values = [row[4] for row in past_records if row[4] is not None]
    bs_values = [row[5] for row in past_records if row[5] is not None]
    hr_values = [row[7] for row in past_records if row[7] is not None]
    risk_values = [str(row[8]).lower() for row in past_records if row[8] is not None]

    if systolic_values:
        avg_systolic = sum(systolic_values) / len(systolic_values)
        if latest_systolic > avg_systolic + 10:
            worsening_points += 1
            reasons.append("Systolic BP has increased compared to recent visits.")
        elif latest_systolic < avg_systolic - 10:
            improving_points += 1
            reasons.append("Systolic BP has improved compared to recent visits.")

    if diastolic_values:
        avg_diastolic = sum(diastolic_values) / len(diastolic_values)
        if latest_diastolic > avg_diastolic + 5:
            worsening_points += 1
            reasons.append("Diastolic BP has increased compared to recent visits.")
        elif latest_diastolic < avg_diastolic - 5:
            improving_points += 1
            reasons.append("Diastolic BP has improved compared to recent visits.")

    if bs_values:
        avg_bs = sum(bs_values) / len(bs_values)
        if latest_bs > avg_bs + 1:
            worsening_points += 1
            reasons.append("Blood sugar is rising compared to recent visits.")
        elif latest_bs < avg_bs - 1:
            improving_points += 1
            reasons.append("Blood sugar has improved compared to recent visits.")

    if hr_values:
        avg_hr = sum(hr_values) / len(hr_values)
        if latest_hr > avg_hr + 10:
            worsening_points += 1
            reasons.append("Heart rate is higher than recent visits.")
        elif latest_hr < avg_hr - 10:
            improving_points += 1
            reasons.append("Heart rate has improved compared to recent visits.")

    high_risk_count = risk_values.count("high risk")
    mid_risk_count = risk_values.count("mid risk")

    if high_risk_count >= 2:
        worsening_points += 2
        reasons.append("Recent history shows repeated high-risk predictions.")
    elif mid_risk_count >= 2:
        worsening_points += 1
        reasons.append("Recent history shows repeated mid-risk predictions.")

    continuity_score = worsening_points - improving_points

    if continuity_score >= 3:
        trend_status = "critical worsening"
        alert = "Patient condition is worsening significantly over recent visits."
    elif continuity_score >= 1:
        trend_status = "worsening"
        alert = "Patient shows signs of deterioration compared to recent visits."
    elif continuity_score <= -2:
        trend_status = "improving"
        alert = "Patient condition appears to be improving over time."
    else:
        trend_status = "stable"
        alert = "No major trend change detected from recent visits."

    return {
        "trend_status": trend_status,
        "alert": alert,
        "continuity_score": continuity_score,
        "reasons": reasons
    }