import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "ml" / "saved_models"

recovery_model = joblib.load(MODEL_DIR / "recovery_model.pkl")

recovery_disease_encoder = joblib.load(MODEL_DIR / "recovery_disease_encoder.pkl")

severity_encoder = joblib.load(MODEL_DIR / "severity_encoder.pkl")

treatment_encoder = joblib.load(MODEL_DIR / "treatment_encoder.pkl")


def predict_recovery(
    disease,
    severity,
    treatment,
    age
):

    encoded_disease = recovery_disease_encoder.transform(
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

    prediction = recovery_model.predict(features)

    return {
        "expected_recovery_days": round(
            prediction[0],
            1
        )
    }