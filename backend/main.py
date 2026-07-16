from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import joblib
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db
from models import Base, Patient
from schemas import PatientResponse, PredictionRequest, TreatmentRequest, RecoveryRequest, ComplicationRequest
from symptom_surveillance import get_symptom_counts,detect_emerging_symptoms
from treatment_effectiveness import (calculate_treatment_effectiveness)
from disease_treatment_effectiveness import (disease_treatment_effectiveness)
from outbreak_risk import (calculate_outbreak_risk)
from federated_metrics import get_federated_metrics
from regional_outbreaks import (regional_outbreaks)
from novel_symptom_detection import (detect_novel_symptoms)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("disease_model.pkl")
symptom_encoder = joblib.load("symptom_encoder.pkl")
disease_encoder = joblib.load("disease_encoder.pkl")
recovery_model = joblib.load("recovery_model.pkl")

recovery_disease_encoder = joblib.load("recovery_disease_encoder.pkl")

severity_encoder = joblib.load("severity_encoder.pkl")

treatment_encoder = joblib.load("treatment_encoder.pkl")

complication_model = joblib.load("complication_model.pkl")

complication_disease_encoder = joblib.load("complication_disease_encoder.pkl")

complication_severity_encoder = joblib.load("complication_severity_encoder.pkl")

complication_treatment_encoder = joblib.load("complication_treatment_encoder.pkl")

complication_label_encoder = joblib.load("complication_label_encoder.pkl")

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "API Working"}

@app.get("/patients", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return patients

@app.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):

    total_patients = db.query(Patient).count()

    disease_counts = (
        db.query(
            Patient.disease,
            func.count(Patient.id)
        )
        .group_by(Patient.disease)
        .all()
    )

    hospital_counts = (
        db.query(
            Patient.hospital,
            func.count(Patient.id)
        )
        .group_by(Patient.hospital)
        .all()
    )

    return {
        "total_patients": total_patients,
        "disease_distribution": {
            disease: count
            for disease, count in disease_counts
        },
        "hospital_distribution": {
            hospital: count
            for hospital, count in hospital_counts
        }
    }

@app.post("/predict")
def predict_disease(request: PredictionRequest):

    encoded_symptom = symptom_encoder.transform(
        [request.symptoms]
    )

    prediction = model.predict(
    encoded_symptom.reshape(-1, 1)
    )

    probabilities = model.predict_proba(
        encoded_symptom.reshape(-1, 1)
    )

    confidence = max(probabilities[0]) * 100

    disease = disease_encoder.inverse_transform(
        prediction
    )[0]

    return {
        "symptoms": request.symptoms,
        "predicted_disease": disease,
        "confidence": round(confidence, 2)
    }

@app.post("/recommend-treatment")
def recommend_treatment(
    request: TreatmentRequest,
    db: Session = Depends(get_db)
):

    patients = db.query(Patient).filter(
        Patient.disease == request.disease
    ).all()

    if not patients:
        return {
            "error": "Disease not found"
        }

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
        "disease": request.disease,
        "recommended_treatment": best_treatment,
        "success_rate": round(best_rate, 2)
    }

@app.get("/disease-trends/{disease}")
def get_disease_trends(
    disease: str,
    db: Session = Depends(get_db)
):

    trends = (
        db.query(
            Patient.visit_date,
            func.count(Patient.id)
        )
        .filter(
            Patient.disease == disease
        )
        .group_by(Patient.visit_date)
        .order_by(Patient.visit_date)
        .all()
    )

    return [
        {
            "date": str(date),
            "cases": count
        }
        for date, count in trends
    ]

@app.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db)
):

    diseases = (
        db.query(
            Patient.disease,
            func.count(Patient.id)
        )
        .group_by(Patient.disease)
        .all()
    )

    alerts = []

    for disease, count in diseases:

        if count > 100:

            alerts.append({
                "disease": disease,
                "cases": count,
                "alert": "Potential outbreak detected"
            })

    return alerts

@app.get("/symptom-trends")
def symptom_trends():

    return get_symptom_counts()

@app.get("/emerging-symptoms")
def emerging_symptoms():

    return detect_emerging_symptoms()

@app.get("/treatment-effectiveness")
def treatment_effectiveness():

    return (
        calculate_treatment_effectiveness()
    )

@app.get(
    "/disease-treatment-effectiveness"
)
def treatment_rankings():

    return (
        disease_treatment_effectiveness()
    )

@app.get("/outbreak-risk")
def outbreak_risk():

    return (
        calculate_outbreak_risk()
    )

@app.get("/federated-metrics")
def federated_metrics():
    return get_federated_metrics()

@app.get("/regional-outbreaks")
def get_regional_outbreaks():

    return regional_outbreaks()

@app.get("/novel-symptoms")
def novel_symptoms():

    return detect_novel_symptoms()

@app.post("/predict-recovery")
def predict_recovery(request: RecoveryRequest):
    encoded_disease = recovery_disease_encoder.transform(
    [request.disease]
    )[0]
    encoded_severity = severity_encoder.transform(
    [request.severity]
    )[0]
    encoded_treatment = treatment_encoder.transform(
    [request.treatment]
    )[0]
    features = [[
    encoded_disease,
    encoded_severity,
    encoded_treatment,
    request.age
    ]]
    prediction = recovery_model.predict(features)
    return {
    "expected_recovery_days": round(
        prediction[0],
        1
    )
    }

@app.post("/predict-complication")
def predict_complication(
    request: ComplicationRequest
):
    encoded_disease = complication_disease_encoder.transform([request.disease])[0]
    

    encoded_severity = complication_severity_encoder.transform([request.severity])[0]

    encoded_treatment = complication_treatment_encoder.transform([request.treatment])[0]
    features = [[
    encoded_disease,
    encoded_severity,
    encoded_treatment,
    request.age
    ]]
    prediction = complication_model.predict(features)
    probabilities = complication_model.predict_proba(features)

    yes_probability = probabilities[0][1] * 100
    none_probability = probabilities[0][0] * 100
    if yes_probability < 30:
        risk_level = "Low"

    elif yes_probability < 70:
        risk_level = "Moderate"

    else:
        risk_level = "High"

    
    result = complication_label_encoder.inverse_transform(prediction)[0]
    confidence = max(probabilities[0]) * 100
    return {
    "complication_prediction": result,
    "risk_level": risk_level,
    "probability_of_complication": round(
        yes_probability,
        2
    ),
    "confidence": round(
        confidence,
        2
    )
    }


