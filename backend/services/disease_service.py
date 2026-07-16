import joblib

model = joblib.load("disease_model.pkl")
symptom_encoder = joblib.load("symptom_encoder.pkl")
disease_encoder = joblib.load("disease_encoder.pkl")


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