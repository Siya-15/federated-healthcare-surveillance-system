import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "ml" / "saved_models"

complication_model = joblib.load(MODEL_DIR / "complication_model.pkl")

disease_encoder = joblib.load(MODEL_DIR / "complication_disease_encoder.pkl")

severity_encoder = joblib.load(MODEL_DIR / "complication_severity_encoder.pkl")

treatment_encoder = joblib.load(MODEL_DIR / "complication_treatment_encoder.pkl")

label_encoder = joblib.load(MODEL_DIR / "complication_label_encoder.pkl")


def predict_complication(
    disease,
    severity,
    treatment,
    age
):

    encoded_disease = disease_encoder.transform(
        [disease]
    )[0]

    encoded_severity = severity_encoder.transform(
        [severity]
    )[0]

    encoded_treatment = treatment_encoder.transform(
        [treatment]
    )[0]

    features = [[
        encoded_disease,
        encoded_severity,
        encoded_treatment,
        age
    ]]

    prediction = complication_model.predict(features)

    probabilities = complication_model.predict_proba(
        features
    )

    yes_probability = probabilities[0][1] * 100

    confidence = max(probabilities[0]) * 100

    if yes_probability < 30:
        risk_level = "Low"
    elif yes_probability < 70:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    return {
        "complication_prediction":
            label_encoder.inverse_transform(prediction)[0],
        "risk_level": risk_level,
        "probability_of_complication":
            round(yes_probability, 2),
        "confidence":
            round(confidence, 2)
    }