from collections import defaultdict

from database import SessionLocal
from models import Patient


def regional_outbreaks():

    db = SessionLocal()

    patients = db.query(Patient).all()

    hospital_symptoms = defaultdict(
        lambda: defaultdict(int)
    )

    for patient in patients:

        symptoms = (
            patient.symptoms.split(",")
        )

        for symptom in symptoms:

            hospital_symptoms[
                patient.hospital
            ][symptom] += 1

    results = []

    for hospital, symptom_data in (
        hospital_symptoms.items()
    ):

        for symptom, count in (
            symptom_data.items()
        ):

            if count > 80:
                risk = "HIGH"

            elif count > 40:
                risk = "MEDIUM"

            else:
                risk = "LOW"

            results.append({

                "hospital":
                    hospital,

                "symptom":
                    symptom,

                "cases":
                    count,

                "risk":
                    risk
            })

    db.close()

    return sorted(
        results,
        key=lambda x:
            x["cases"],
        reverse=True
    )