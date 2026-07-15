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

disease_profiles = {

    "Flu": {
        "severity": ["Mild", "Moderate"],
        "recovery": (3, 7),
        "complication_probability": 0.05
    },

    "Covid": {
        "severity": ["Moderate", "Severe"],
        "recovery": (7, 14),
        "complication_probability": 0.15
    },

    "Dengue": {
        "severity": ["Moderate", "Severe"],
        "recovery": (8, 15),
        "complication_probability": 0.20
    },

    "Malaria": {
        "severity": ["Moderate", "Severe"],
        "recovery": (10, 18),
        "complication_probability": 0.25
    }

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

    profile = disease_profiles[disease]
    severity = choice(
        profile["severity"]
    )

    recovery_days = randint(
    profile["recovery"][0],
    profile["recovery"][1]
    )

    complications = (
    "Yes"
    if random() <
    profile["complication_probability"]
    else "None"
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

    probability = success_probability[treatment]

    if severity == "Severe":
        probability -= 0.15

    elif severity == "Moderate":
        probability -= 0.05

    if complications == "Yes":
        probability -= 0.10

    outcome = (
        "Recovered"
        if random() < probability
        else "Under Treatment"
    )

    patient = Patient(
        hospital=choice(hospitals),
        district=choice([
            "Vellore",
            "Chennai",
            "Bangalore"
        ]),
        age=randint(18, 80),
        gender=choice(["Male", "Female"]),
        occupation=choice([
            "Student",
            "Farmer",
            "Teacher",
            "Healthcare Worker",
            "Office Worker"
        ]),
        symptoms=",".join(symptoms),
        severity=severity,
        symptom_duration=randint(1,10),
        disease=disease,
        treatment=treatment,
        outcome=outcome,

        recovery_days=recovery_days,

        complications=complications,

        visit_date=date.today() -
            timedelta(days=randint(0,60))
    )

    db.add(patient)

db.commit()
db.close()

print("500 patient records inserted successfully!")