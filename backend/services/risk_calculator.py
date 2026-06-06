from model.predict import predict_risk
from backend.services.recommendation import get_recommendation
from backend.services.continuity_analyzer import analyze_continuity

def calculate_risk(data: dict):
    prediction_result = predict_risk(data)

    risk_level = prediction_result["predicted_label"]
    confidence = prediction_result["confidence"]
    class_probabilities = prediction_result["class_probabilities"]

    continuity_result = analyze_continuity(data)

    recommendation = get_recommendation(risk_level)

    return {
        "risk_level": risk_level,
        "confidence": confidence,
        "class_probabilities": class_probabilities,
        "recommendation": recommendation,
        "continuity": continuity_result
    }