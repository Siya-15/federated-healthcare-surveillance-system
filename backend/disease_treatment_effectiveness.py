from database import SessionLocal
from models import Patient


def disease_treatment_effectiveness():

    db = SessionLocal()

    patients = db.query(Patient).all()

    disease_stats = {}

    for patient in patients:

        disease = patient.disease
        treatment = patient.treatment

        if disease not in disease_stats:
            disease_stats[disease] = {}

        if treatment not in disease_stats[disease]:

            disease_stats[disease][treatment] = {
                "total": 0,
                "recovered": 0
            }

        disease_stats[disease][
            treatment
        ]["total"] += 1

        if patient.outcome == "Recovered":

            disease_stats[disease][
                treatment
            ]["recovered"] += 1

    results = {}

    for disease, treatments in disease_stats.items():

        results[disease] = []

        for treatment, stats in treatments.items():

            effectiveness = (
                stats["recovered"]
                / stats["total"]
            ) * 100

            results[disease].append({
                "treatment": treatment,
                "effectiveness":
                    round(effectiveness, 2)
            })

        results[disease].sort(
            key=lambda x:
                x["effectiveness"],
            reverse=True
        )

    db.close()

    return results