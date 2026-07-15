from database import SessionLocal
from models import Patient

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

db = SessionLocal()

patients = db.query(Patient).all()

data = []

for p in patients:
    data.append({
        "disease": p.disease,
        "severity": p.severity,
        "treatment": p.treatment,
        "age": p.age,
        "recovery_days": p.recovery_days
    })

df = pd.DataFrame(data)

disease_encoder = LabelEncoder()
severity_encoder = LabelEncoder()
treatment_encoder = LabelEncoder()

df["disease"] = disease_encoder.fit_transform(df["disease"])
df["severity"] = severity_encoder.fit_transform(df["severity"])
df["treatment"] = treatment_encoder.fit_transform(df["treatment"])

X = df[[
    "disease",
    "severity",
    "treatment",
    "age"
]]

y = df["recovery_days"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "recovery_model.pkl")
joblib.dump(disease_encoder, "recovery_disease_encoder.pkl")
joblib.dump(severity_encoder, "severity_encoder.pkl")
joblib.dump(treatment_encoder, "treatment_encoder.pkl")

print("Recovery model trained successfully")