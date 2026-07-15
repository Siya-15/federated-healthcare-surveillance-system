from utils import train_local_model

datasets = [
    "hospital_a.csv",
    "hospital_b.csv",
    "hospital_c.csv"
]

accuracies = []

print("\nLOCAL MODELS\n")

for dataset in datasets:

    model, accuracy = train_local_model(
        dataset
    )

    accuracies.append(accuracy)

    print(
        f"{dataset}: "
        f"{accuracy:.4f}"
    )

global_accuracy = (
    sum(accuracies)
    / len(accuracies)
)

print("\nFEDERATED MODEL\n")

print(
    f"Global Accuracy: "
    f"{global_accuracy:.4f}"
)