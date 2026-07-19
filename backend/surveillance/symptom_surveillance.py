from collections import Counter
from datetime import date, timedelta

from database import SessionLocal
from models import Patient



def calculate_symptom_surveillance():

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
        for symptom in patient.symptoms.split(","):
            current_counts[symptom.strip()] += 1
        

    for patient in previous_patients:
        for symptom in patient.symptoms.split(","):
            previous_counts[symptom.strip()] += 1

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
            growth_percent = None
            trend = "New"

        else:
            growth_percent = (
                (
                    current - previous
                )
                /
                previous
            ) * 100

        if current < 10:
            alert = "LOW"

        elif growth_percent >= 100:
            alert = "CRITICAL"

        elif growth_percent >= 50:
            alert = "HIGH"

        elif growth_percent >= 20:
            alert = "MEDIUM"

        else:
            alert = "LOW"

        if current > previous:
            trend = "Increasing"
        elif current < previous:
            trend = "Decreasing"
        else:
            trend = "Stable"

        results.append({

            "symptom":symptom,
            "current_cases":current,
            "previous_cases":previous,
            "growth_percent":round(growth_percent, 2),
            "trend":trend,
            "alert_level":alert
        })

    db.close()

    return sorted(
        results,
        key=lambda x:
            x["growth_percent"],
        reverse=True
    )