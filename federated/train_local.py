import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("hospital_a.csv")

print(df.head())

symptom_encoder = LabelEncoder()
disease_encoder = LabelEncoder()

df["symptoms"] = symptom_encoder.fit_transform(
    df["symptoms"]
)

df["disease"] = disease_encoder.fit_transform(
    df["disease"]
)

X = df[["symptoms"]]
y = df["disease"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = DecisionTreeClassifier()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"Accuracy: {accuracy:.4f}"
)