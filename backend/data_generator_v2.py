from faker import Faker
from random import choice, randint, random
from datetime import date, timedelta

from database import SessionLocal
from models import Patient
from services.severity_service import predict_severity

fake = Faker()

db = SessionLocal()

hospitals = [
    "Hospital A",
    "Hospital B",
    "Hospital C"
]

DISEASES = {
    "Flu": {
        "symptoms": {
            "fever": 0.90,
            "cough": 0.80,
            "sore_throat": 0.65,
            "fatigue": 0.55,
            "headache": 0.30,
        },
        "base_severity": 1,
        "recovery_range": (3, 7),
        "treatments": [
            "Paracetamol",
            "Ibuprofen",
            "Rest & Hydration"
        ],
        "complication_probability": 0.05
    },

    "Covid": {
        "symptoms": {
            "fever": 0.90,
            "cough": 0.85,
            "fatigue": 0.80,
            "loss_of_smell": 0.45,
            "headache": 0.35,
        },
        "base_severity": 2,
        "recovery_range": (7, 14),
        "treatments": [
            "Antiviral",
            "Supportive Care",
            "Oxygen Therapy"
        ],
        "complication_probability": 0.15
    },

    "Dengue": {
        "symptoms": {
            "fever": 0.95,
            "headache": 0.80,
            "rash": 0.50,
            "nausea": 0.45,
            "fatigue": 0.40,
        },
        "base_severity": 2,
        "recovery_range": (8, 15),
        "treatments": [
            "IV Fluids",
            "Electrolytes",
            "Supportive Care"
        ],
        "complication_probability": 0.20
    },

    "Malaria": {
        "symptoms": {
            "fever": 0.95,
            "chills": 0.90,
            "sweating": 0.80,
            "headache": 0.55,
            "fatigue": 0.40,
        },
        "base_severity": 3,
        "recovery_range": (10, 18),
        "treatments": [
            "Antimalarial",
            "IV Fluids",
            "Supportive Care"
        ],
        "complication_probability": 0.25
    }
}

def generate_symptoms(profile):
    symptoms = []

    for symptom, probability in profile["symptoms"].items():
        if random() < probability:
            symptoms.append(symptom)

    if len(symptoms) == 0:
        symptoms.append(
            max(
                profile["symptoms"],
                key=profile["symptoms"].get
            )
        )

    return symptoms

def calculate_severity(age, symptom_duration, symptoms, profile):
    severity_score = profile["base_severity"]

    # Age
    if age >= 65:
        severity_score += 1

    # Duration
    if symptom_duration >= 7:
        severity_score += 1

    # Symptom burden
    if len(symptoms) >= 4:
        severity_score += 1
        
        
    if severity_score <= 1:
        severity = "Mild"
    elif severity_score <= 3:
        severity = "Moderate"
    else:
        severity = "Severe"
    return severity
    
def calculate_complications(age, severity, treatment, profile):
    probability = profile["complication_probability"]

    # Older patients are at higher risk
    if age >= 60:
        probability += 0.15

    # Severe cases are more likely to develop complications
    if severity == "Severe":
        probability += 0.10

    # Effective treatments reduce the risk
    if treatment in ["Antiviral", "Antimalarial"]:
        probability -= 0.05

    # Keep probability between 0 and 0.95
    probability = max(0, min(probability, 0.95))

    return "Yes" if random() < probability else "None"

def calculate_recovery(age, severity, complications, profile):
    recovery_days = randint(
        profile["recovery_range"][0],
        profile["recovery_range"][1]
    )

    if severity == "Severe":
        recovery_days += randint(3, 6)

    if complications == "Yes":
        recovery_days += randint(2, 5)

    if age >= 60:
        recovery_days += randint(1, 3)

    return recovery_days

def determine_outcome(treatment, severity, complications):
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

    probability = max(0.05, min(probability, 0.99))

    return (
        "Recovered"
        if random() < probability
        else "Under Treatment"
    )

for _ in range(2000):

    # ------------------------
    # Basic Patient Information
    # ------------------------

    disease = choice(list(DISEASES.keys()))
    profile = DISEASES[disease]

    age = randint(18, 80)

    symptom_duration = randint(1, 10)

    symptoms = generate_symptoms(profile)

    severity = calculate_severity(
        age,
        symptom_duration,
        symptoms,
        profile
    )

    treatment = choice(profile["treatments"])

    complications = calculate_complications(
        age,
        severity,
        treatment,
        profile
    )

    recovery_days = calculate_recovery(
        age,
        severity,
        complications,
        profile
    )

    outcome = determine_outcome(
        treatment,
        severity,
        complications
    )

    patient = Patient(
        hospital=choice(hospitals),
        district=choice([
            "Vellore",
            "Chennai",
            "Bangalore"
        ]),
        age=age,
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
        symptom_duration=symptom_duration,
        disease=disease,
        treatment=treatment,
        outcome=outcome,
        recovery_days=recovery_days,
        complications=complications,
        visit_date=date.today() - timedelta(days=randint(0, 60))
    )

    db.add(patient)

db.commit()
db.close()