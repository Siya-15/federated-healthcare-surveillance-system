import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

SYMPTOMS = [
    "fever",
    "cough",
    "fatigue",
    "headache",
    "chills",
    "nausea",
    "rash",
    "sore_throat",
    "loss_of_smell",
    "sweating"
]


def train_local_model(csv_file):

    df = pd.read_csv(csv_file)

    for symptom in SYMPTOMS:

        df[symptom] = df["symptoms"].apply(
            lambda x:
            1 if symptom in x.split(",")
            else 0
        )

    
    disease_encoder = LabelEncoder()

    df["disease"] = disease_encoder.fit_transform(
        df["disease"]
    )

    X = df[SYMPTOMS]
    y = df["disease"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )
    )

    model = DecisionTreeClassifier()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    return model, accuracy