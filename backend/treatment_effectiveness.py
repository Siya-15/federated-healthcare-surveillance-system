from database import SessionLocal
from models import Patient


def calculate_treatment_effectiveness():

    db = SessionLocal()

    patients = db.query(Patient).all()

    treatment_stats = {}

    for patient in patients:

        treatment = patient.treatment

        if treatment not in treatment_stats:

            treatment_stats[treatment] = {
                "total": 0,
                "recovered": 0
            }

        treatment_stats[treatment]["total"] += 1

        if patient.outcome == "Recovered":

            treatment_stats[treatment][
                "recovered"
            ] += 1

    results = []

    for treatment, stats in treatment_stats.items():

        effectiveness = (
            stats["recovered"]
            / stats["total"]
        ) * 100

        results.append({
            "treatment": treatment,
            "effectiveness":
                round(effectiveness, 2)
        })

    db.close()

    return sorted(
        results,
        key=lambda x:
            x["effectiveness"],
        reverse=True
    )