from pathlib import Path
import joblib
import pandas as pd
import os


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "ml" / "saved_models"

model = joblib.load(MODEL_DIR / "severity_model.pkl")
mlb = joblib.load(MODEL_DIR / "symptom_encoder.pkl")
feature_columns = joblib.load(MODEL_DIR / "severity_features.pkl")


#Step 3: Create the prediction function
def predict_severity(
    age,
    disease,
    symptoms,
    symptom_duration
):
    #Step 4: Encode symptoms
    
    symptom_features = mlb.transform([symptoms])
    
    #Step 5: Convert to DataFrame
    symptom_df = pd.DataFrame(
        symptom_features,
        columns=mlb.classes_
    )
    #Step 6: Disease encoding
    disease_data = {
        "disease_Covid": 0,
        "disease_Dengue": 0,
        "disease_Flu": 0,
        "disease_Malaria": 0
    }

    disease_data[f"disease_{disease}"] = 1
    disease_df = pd.DataFrame([disease_data])

    #Step 7: Create the numeric features
    numeric_df = pd.DataFrame(
        [{
            "age": age,
            "symptom_duration": symptom_duration
        }]
    )

    #Step 8: Combine everything
    X = pd.concat(
        [
            numeric_df,
            disease_df,
            symptom_df
        ],
        axis=1
    )

    #step 9:Match the training feature order
    X = X.reindex(
        columns=feature_columns,
        fill_value=0
    )

    #step10:predict
    probabilities = model.predict_proba(X)[0]
    prediction = model.predict(X)[0]

    confidence = round(max(probabilities) * 100, 2)

    return {
        "severity": prediction,
        "confidence": confidence
    }


