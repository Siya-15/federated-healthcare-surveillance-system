from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "ml" / "saved_models"


model = joblib.load(MODEL_DIR / "disease_model.pkl")
symptom_encoder = joblib.load(MODEL_DIR / "symptom_encoder.pkl")
disease_encoder = joblib.load(MODEL_DIR / "disease_encoder.pkl")


def predict_disease(symptoms):

    encoded = symptom_encoder.transform([symptoms])

    prediction = model.predict(
        encoded.reshape(-1, 1)
    )

    probabilities = model.predict_proba(
        encoded.reshape(-1, 1)
    )

    disease = disease_encoder.inverse_transform(
        prediction
    )[0]

    confidence = max(probabilities[0]) * 100


    return {
        "predicted_disease": disease,
        "confidence": round(confidence, 2)
    }

