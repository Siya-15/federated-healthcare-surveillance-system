from collections import Counter
from datetime import date, timedelta

from database import SessionLocal
from models import Patient
from config.disease_profiles import DISEASES


def calculate_disease_surveillance():

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
        current_counts[patient.disease] += 1

    for patient in previous_patients:
        previous_counts[patient.disease] += 1

    results = []

    all_diseases = set(
        current_counts.keys()
    ).union(
        previous_counts.keys()
    )

    for disease in all_diseases:

        current = current_counts[disease]

        previous = previous_counts[disease]

        if previous == 0:

            growth_percent = 100

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

            "disease": disease,
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