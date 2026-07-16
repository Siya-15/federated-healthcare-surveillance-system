from models import Patient


def get_best_treatment(disease, db):

    patients = db.query(Patient).filter(
        Patient.disease == disease
    ).all()

    if not patients:
        return None

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
            treatment_stats[treatment]["recovered"] += 1

    best_treatment = None
    best_rate = -1

    for treatment, stats in treatment_stats.items():

        success_rate = (
            stats["recovered"] /
            stats["total"]
        ) * 100

        if success_rate > best_rate:
            best_rate = success_rate
            best_treatment = treatment

    return {
        "recommended_treatment": best_treatment,
        "success_rate": round(best_rate, 2)
    }