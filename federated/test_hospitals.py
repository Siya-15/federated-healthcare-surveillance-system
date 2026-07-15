from utils import train_local_model

datasets = [
    "hospital_a.csv",
    "hospital_b.csv",
    "hospital_c.csv"
]

for dataset in datasets:

    model, accuracy = train_local_model(
        dataset
    )

    print(
        f"{dataset}: {accuracy:.4f}"
    )