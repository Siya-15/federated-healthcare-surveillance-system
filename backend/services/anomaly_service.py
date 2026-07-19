#load the model
from pathlib import Path
import joblib
import pandas as pd
from config.disease_profiles import DISEASES

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "ml" / "saved_models"

model = joblib.load(MODEL_DIR / "anomaly_model.pkl")
mlb = joblib.load(MODEL_DIR / "anomaly_symptom_mlb.pkl")
feature_columns = joblib.load(MODEL_DIR / "anomaly_features.pkl")

#create the prediction function
def detect_novel_symptoms(age, disease, symptoms):
    symptom_features = mlb.transform([symptoms])

    #symptoms
    symptom_df = pd.DataFrame(
        symptom_features,
        columns=mlb.classes_
    )

    #diseases
    disease_df = pd.DataFrame(
        [{disease: 1}]
    )

    #age
    numeric_df = pd.DataFrame({
        "age": [age]
    })

    #combine everything
    X = pd.concat(
        [
            numeric_df,
            disease_df,
            symptom_df
        ],
        axis=1
    )

    #align columns
    X = X.reindex(
        columns=feature_columns,
        fill_value=0
    )

    #predict
    prediction = model.predict(X)[0]
    score = model.decision_function(X)[0]

    #determine status
    status = (
        "Possible Novel Pattern"
        if prediction == -1
        else "Normal"
    )

    #calculate risk level
    if score > 0.1:
        risk = "Low"

    elif score > 0:
        risk = "Moderate"

    else:
        risk = "High"

    #find unexpected symptoms
    typical_symptoms = DISEASES[disease]["symptoms"]
    unexpected = []

    for symptom in symptoms:
        if symptom not in typical_symptoms:
            unexpected.append(symptom)
    
    #recommendation
    if prediction == -1:
        recommendation = (
            "Consider additional diagnostic testing "
            "and monitor for similar cases."
        )
    else:
        recommendation = "Symptoms are consistent with the predicted disease."

    return {
        "status":status,
        "anomaly_score": round(float(score), 4),
        "risk_level": risk,
        "unexpected_symptoms": unexpected,
        "recommendation": recommendation
    }

#test it
if __name__ == "__main__":

    result = detect_novel_symptoms(
        age=65,
        disease="Flu",
        symptoms=[
            "rash",
            "joint pain",
            "red eyes",
            "vomiting"
        ]
    )

    print(result)
