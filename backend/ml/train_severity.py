import pandas as pd
from sqlalchemy import create_engine
import joblib
import os

#import the required libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

#import the encoders
from sklearn.preprocessing import MultiLabelBinarizer

DATABASE_URL = "postgresql+psycopg2://postgres:Chotus_1505@localhost:5432/healthcare_db"
engine = create_engine(DATABASE_URL)

df = pd.read_sql(
    "SELECT * FROM patients",
    engine
)

#Convert symptom strings into lists
df["symptoms"] = df["symptoms"].apply(
    lambda x: x.split(",")
)

#Apply MultiLabelBinarizer
mlb = MultiLabelBinarizer()


symptom_features = mlb.fit_transform(
    df["symptoms"]
)

#convert into dataframe
symptom_df = pd.DataFrame(
    symptom_features,
    columns=mlb.classes_
)

#one-hot encoding for diseases
disease_df = pd.get_dummies(
    df["disease"],
    prefix="disease"
)

#build the numerical features
numeric_df = df[
    [
        "age",
        "symptom_duration"
    ]
]

X = pd.concat(
    [
        numeric_df,
        disease_df,
        symptom_df
    ],
    axis=1
)

y = df["severity"]

#split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

#train the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

#make predictions
y_pred = model.predict(X_test)


#save the model
os.makedirs("saved_models", exist_ok=True)

joblib.dump(model, "saved_models/severity_model.pkl")
joblib.dump(mlb, "saved_models/symptom_encoder.pkl")
joblib.dump(list(X.columns), "saved_models/severity_features.pkl")

print("Severity model saved successfully!")
