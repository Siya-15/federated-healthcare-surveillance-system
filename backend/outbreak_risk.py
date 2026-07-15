from collections import Counter
from datetime import date, timedelta

from database import SessionLocal
from models import Patient


def calculate_outbreak_risk():

    db = SessionLocal()

    today = date.today()

    current_start = today - timedelta(days=30)

    previous_start = today - timedelta(days=60)

    current_patients = (
        db.query(Patient)
        .filter(Patient.visit_date >= current_start)
        .all()
    )

    previous_patients = (
        db.query(Patient)
        .filter(
            Patient.visit_date >= previous_start,
            Patient.visit_date < current_start
        )
        .all()
    )

    current_counts = Counter()

    previous_counts = Counter()

    for patient in current_patients:

        symptoms = patient.symptoms.split(",")

        for symptom in symptoms:

            current_counts[symptom] += 1

    for patient in previous_patients:

        symptoms = patient.symptoms.split(",")

        for symptom in symptoms:

            previous_counts[symptom] += 1

    results = []

    all_symptoms = set(
        current_counts.keys()
    ).union(
        previous_counts.keys()
    )

    for symptom in all_symptoms:

        current = current_counts[symptom]

        previous = previous_counts[symptom]

        if previous == 0:

            increase_percent = 100

        else:

            increase_percent = (
                (
                    current - previous
                )
                /
                previous
            ) * 100

        if increase_percent > 75:

            risk = "HIGH"

        elif increase_percent > 25:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        results.append({

            "symptom": symptom,

            "current_period":
                current,

            "previous_period":
                previous,

            "increase_percent":
                round(
                    increase_percent,
                    2
                ),

            "risk":
                risk
        })

    db.close()

    return sorted(
        results,
        key=lambda x:
            x["increase_percent"],
        reverse=True
    )