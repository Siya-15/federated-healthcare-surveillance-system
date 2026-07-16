from database import SessionLocal
from models import Patient

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
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
        "complications": p.complications
    })

df = pd.DataFrame(data)

# --------------------------
# Label Encoding
# --------------------------

disease_encoder = LabelEncoder()
severity_encoder = LabelEncoder()
treatment_encoder = LabelEncoder()
complication_encoder = LabelEncoder()

df["disease"] = disease_encoder.fit_transform(df["disease"])
df["severity"] = severity_encoder.fit_transform(df["severity"])
df["treatment"] = treatment_encoder.fit_transform(df["treatment"])
df["complications"] = complication_encoder.fit_transform(
    df["complications"]
)

# --------------------------
# Features and Target
# --------------------------

X = df[
    [
        "disease",
        "severity",
        "treatment",
        "age"
    ]
]

y = df["complications"]

# --------------------------
# Train Model
# --------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# --------------------------
# Save Everything
# --------------------------

joblib.dump(
    model,
    "complication_model.pkl"
)

joblib.dump(
    disease_encoder,
    "complication_disease_encoder.pkl"
)

joblib.dump(
    severity_encoder,
    "complication_severity_encoder.pkl"
)

joblib.dump(
    treatment_encoder,
    "complication_treatment_encoder.pkl"
)

joblib.dump(
    complication_encoder,
    "complication_label_encoder.pkl"
)

print("Complication model trained successfully!")