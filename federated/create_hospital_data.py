import pandas as pd
from faker import Faker
from random import choice, randint, random
from datetime import date, timedelta

fake = Faker()

all_symptoms = [
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

disease_data = {

    "Flu": [
        ["fever", "cough"],
        ["fever", "sore_throat"],
        ["cough", "fatigue"],
        ["fever", "cough", "fatigue"]
    ],

    "Covid": [
        ["fever", "fatigue"],
        ["cough", "loss_of_smell"],
        ["fever", "cough", "fatigue"],
        ["fatigue", "loss_of_smell"]
    ],

    "Dengue": [
        ["fever", "headache"],
        ["fever", "rash"],
        ["headache", "nausea"],
        ["fever", "headache", "rash"]
    ],

    "Malaria": [
        ["fever", "chills"],
        ["chills", "sweating"],
        ["fever", "chills", "headache"],
        ["sweating", "fever"]
    ]
}

treatment_data = {

    "Flu": [
        "Paracetamol",
        "Ibuprofen",
        "Rest & Hydration"
    ],

    "Covid": [
        "Antiviral",
        "Supportive Care",
        "Oxygen Therapy"
    ],

    "Dengue": [
        "IV Fluids",
        "Electrolytes",
        "Supportive Care"
    ],

    "Malaria": [
        "Antimalarial",
        "IV Fluids",
        "Supportive Care"
    ]
}


def generate_hospital_data(hospital_name, num_records):

    data = []

    for _ in range(num_records):

        disease = choice(list(disease_data.keys()))
        symptoms = choice(
        disease_data[disease]
        )

        treatment = choice(
            treatment_data[disease]
        )

        success_probability = {
            "Paracetamol": 0.90,
            "Ibuprofen": 0.80,
            "Rest & Hydration": 0.75,

            "Antiviral": 0.92,
            "Supportive Care": 0.78,
            "Oxygen Therapy": 0.85,

            "IV Fluids": 0.88,
            "Electrolytes": 0.82,

            "Antimalarial": 0.91
        }

        data.append({
            "hospital": hospital_name,
            "age": randint(18, 80),
            "gender": choice(["Male", "Female"]),
            "symptoms":",".join(symptoms),
            "disease": disease,
           "treatment": treatment,
            "outcome":
                "Recovered"
                if random() <
                success_probability[treatment]
                else "Under Treatment",
            "visit_date":
                date.today()
                - timedelta(days=randint(0, 60))
        })

    return pd.DataFrame(data)

hospital_a = generate_hospital_data(
    "Hospital A",
    500
)

hospital_b = generate_hospital_data(
    "Hospital B",
    500
)

hospital_c = generate_hospital_data(
    "Hospital C",
    500
)

hospital_a.to_csv(
    "hospital_a.csv",
    index=False
)

hospital_b.to_csv(
    "hospital_b.csv",
    index=False
)

hospital_c.to_csv(
    "hospital_c.csv",
    index=False
)

print("Hospital datasets created!")