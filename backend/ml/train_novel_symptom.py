import joblib
import pandas as pd

from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MultiLabelBinarizer

#read patient data
engine = create_engine(
    "postgresql+psycopg2://postgres:Chotus_1505@localhost:5432/healthcare_db"
)

df = pd.read_sql("SELECT * FROM patients", engine)

#prepare symptoms
df["symptoms"] = df["symptoms"].apply(
    lambda x: x.split(",")
)

mlb = MultiLabelBinarizer()

symptom_df = pd.DataFrame(
    mlb.fit_transform(df["symptoms"]),
    columns=mlb.classes_
)

#disease one-hot encoding
disease_df = pd.get_dummies(df["disease"])

#numeric features
numeric_df = df[["age"]]

#final feature matrix
X = pd.concat(
    [
        numeric_df,
        disease_df,
        symptom_df
    ],
    axis=1
)

#train the isolation forest
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(X)

#save everything
joblib.dump(
    model,
    "saved_models/anomaly_model.pkl"
)

joblib.dump(
    mlb,
    "saved_models/anomaly_symptom_mlb.pkl"
)

joblib.dump(
    list(X.columns),
    "saved_models/anomaly_features.pkl"
)