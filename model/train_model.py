#===========================Importing Libraries===========================#

import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from features import FEATURE_COLUMNS, TARGET_COLUMN

#=========================================================================#

def train():
    print("reading data")
    df = pd.read_csv("data/raw/maternal_health.csv")

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42
    )

    print("training")
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # save_path = os.path.join(base_dir, "models")
    # os.makedirs(save_path, exist_ok=True)

    joblib.dump(model, "model/models/risk_model.pkl")
    joblib.dump(scaler, "model/models/scaler.pkl")
    joblib.dump(encoder, "model/models/encoder.pkl")

    # print("Saving to:", save_path)


if __name__ == "__main__":
    train()

#=========================================================================#