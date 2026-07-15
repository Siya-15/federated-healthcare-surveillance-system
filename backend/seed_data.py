from faker import Faker
from random import choice, randint, random
from datetime import date, timedelta

from database import SessionLocal
from models import Patient

fake = Faker()

db = SessionLocal()

hospitals = [
    "Hospital A",
    "Hospital B",
    "Hospital C"
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



for _ in range(500):

    disease = choice(list(disease_data.keys()))

    symptoms = choice(
    disease_data[disease]
    )

    anomaly_probability = 0.05

    rare_symptoms = [
        "rash",
        "loss_of_smell",
        "chills",
        "sweating",
        "nausea"
    ]

    if random() < anomaly_probability:

        anomaly = choice(
            rare_symptoms
        )

        if anomaly not in symptoms:

            symptoms.append(
                anomaly
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

    patient = Patient(
        hospital=choice(hospitals),
        age=randint(18, 80),
        gender=choice(["Male", "Female"]),
        symptoms=",".join(symptoms),
        disease=disease,
        treatment=treatment,
        outcome=
            "Recovered"
            if random() <
            success_probability[treatment]
            else "Under Treatment",
        visit_date=date.today() - timedelta(days=randint(0, 60))
    )

    db.add(patient)

db.commit()
db.close()

print("500 patient records inserted successfully!")