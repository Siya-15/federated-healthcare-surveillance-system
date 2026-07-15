from collections import defaultdict

from database import SessionLocal
from models import Patient


KNOWN_PATTERNS = {

    "Flu": {
        "fever",
        "cough",
        "fatigue",
        "sore_throat"
    },

    "Covid": {
        "fever",
        "cough",
        "fatigue",
        "loss_of_smell"
    },

    "Dengue": {
        "fever",
        "headache",
        "rash",
        "nausea"
    },

    "Malaria": {
        "fever",
        "chills",
        "sweating",
        "headache"
    }
}


def detect_novel_symptoms():

    db = SessionLocal()

    patients = db.query(Patient).all()

    anomalies = defaultdict(int)

    for patient in patients:

        disease = patient.disease

        symptoms = set(
            patient.symptoms.split(",")
        )

        known = KNOWN_PATTERNS.get(
            disease,
            set()
        )

        unexpected = symptoms - known

        for symptom in unexpected:

            key = (
                disease,
                symptom
            )

            anomalies[key] += 1

    results = []

    for (
        disease,
        symptom
    ), count in anomalies.items():

        results.append({

            "disease":
                disease,

            "unexpected_symptom":
                symptom,

            "count":
                count
        })

    db.close()

    return sorted(
        results,
        key=lambda x:
            x["count"],
        reverse=True
    )