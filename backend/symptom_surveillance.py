from collections import Counter
from database import SessionLocal
from models import Patient

def get_symptom_counts():

    db = SessionLocal()

    patients = db.query(Patient).all()

    symptom_counter = Counter()

    for patient in patients:

        symptoms = patient.symptoms.split(",")

        for symptom in symptoms:

            symptom_counter[symptom] += 1

    db.close()

    return dict(symptom_counter)

def detect_emerging_symptoms():

    symptom_counts = get_symptom_counts()

    alerts = []

    threshold = 100

    for symptom, count in symptom_counts.items():

        if count > threshold:

            alerts.append({
                "symptom": symptom,
                "count": count,
                "alert":
                    f"Emerging symptom detected: {symptom}"
            })

    return alerts