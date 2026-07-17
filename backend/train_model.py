from database import SessionLocal
from models import Patient

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

db = SessionLocal()

patients = db.query(Patient).all()

data = []

for p in patients:
    data.append({
        "symptoms": p.symptoms,
        "disease": p.disease
    })

df = pd.DataFrame(data)

symptom_encoder = LabelEncoder()
disease_encoder = LabelEncoder()
print(df["symptoms"].unique())

X = symptom_encoder.fit_transform(df["symptoms"])
print(symptom_encoder.classes_)
y = disease_encoder.fit_transform(df["disease"])

model = RandomForestClassifier()
model.fit(X.reshape(-1,1), y)

joblib.dump(model, "disease_model.pkl")
joblib.dump(symptom_encoder, "symptom_encoder.pkl")
joblib.dump(disease_encoder, "disease_encoder.pkl")

print("Model trained successfully")