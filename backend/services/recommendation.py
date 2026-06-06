def get_recommendation(risk_level: str, continuity_result: dict = None):
    base_risk = risk_level.lower()

    if continuity_result is None:
        continuity_result = {
            "trend_status": "stable"
        }

    trend_status = continuity_result["trend_status"]

    if base_risk == "low risk":
        if trend_status == "worsening":
            return "Current risk is low, but worsening trend detected. Schedule closer follow-up."
        elif trend_status == "critial worsening":
            return "Current risk is low, but trend is concerning. Clinical review is recommended."
        return "Routine monitoring is recommended."
    
    elif base_risk == "mid risk":
        if trend_status == "worsening":
            return "Doctor consultation is recommended soon, as patient trend is worsening."
        elif trend_status == "critical worsening":
            return "Urgent medical review is recommended due to moderate current risk and worsening trend."
        elif trend_status == "improving":
            return "Moderate risk detected. Continue monitoring and follow prescribed care plan."
        return "Doctor consultation is recommended soon."
    
    elif base_risk == "high risk":
        if trend_status in ["worsening", "critical worsening"]:
            return "Urgent medical attention is strongly recommended. Patient condition is worsening over time."
        return "Urgent medical attention is recommended."

    return "No recommendation available."