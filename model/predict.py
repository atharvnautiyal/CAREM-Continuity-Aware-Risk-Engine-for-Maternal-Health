import os
import pandas as pd
import joblib

from model.features import FEATURE_COLUMNS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "encoder.pkl")


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    encoder = joblib.load(ENCODER_PATH)
    return model, scaler, encoder


def predict_risk(input_data: dict):
    model, scaler, encoder = load_artifacts()

    df = pd.DataFrame([input_data])
    df = df[FEATURE_COLUMNS]

    scaled_data = scaler.transform(df)
    prediction = model.predict(scaled_data)[0]
    predicted_label = encoder.inverse_transform([prediction])[0]

    probabilities = model.predict_proba(scaled_data)[0]

    class_probabilities = {}
    for idx, prob in enumerate(probabilities):
        class_label = encoder.inverse_transform([idx])[0]
        class_probabilities[class_label] = float(prob)

    confidence = max(class_probabilities.values())

    return {
        "predicted_label": predicted_label,
        "confidence": confidence,
        "class_probabilities": class_probabilities
    }