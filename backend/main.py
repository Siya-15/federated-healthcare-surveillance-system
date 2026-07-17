from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import joblib
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db
from models import Base, Patient
from schemas import PatientResponse, PredictionRequest, TreatmentRequest, RecoveryRequest, ComplicationRequest, ClinicalAssessmentRequest
from symptom_surveillance import get_symptom_counts,detect_emerging_symptoms
from treatment_effectiveness import (calculate_treatment_effectiveness)
from disease_treatment_effectiveness import (disease_treatment_effectiveness)
from outbreak_risk import (calculate_outbreak_risk)
from federated_metrics import get_federated_metrics
from regional_outbreaks import (regional_outbreaks)
from novel_symptom_detection import (detect_novel_symptoms)

from services.treatment_service import get_best_treatment
from services.disease_service import predict_disease
from services.recovery_service import predict_recovery
from services.complication_service import predict_complication

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
def predict(
    request: PredictionRequest
):

    return predict_disease(
        request.symptoms
    )

@app.post("/recommend-treatment")
def recommend_treatment(
    request: TreatmentRequest,
    db: Session = Depends(get_db)
):

    result = get_best_treatment(
        request.disease,
        db
    )

    if result is None:
        return {
            "error": "Disease not found"
        }

    return {
        "disease": request.disease,
        **result
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
def recovery_prediction(
    request: RecoveryRequest
):

    return predict_recovery(
        request.disease,
        request.severity,
        request.treatment,
        request.age
    )

@app.post("/predict-complication")
def complication_prediction(
    request: ComplicationRequest
):

    return predict_complication(
        request.disease,
        request.severity,
        request.treatment,
        request.age
    )

@app.post("/clinical-assessment")
def clinical_assessment(
    request: ClinicalAssessmentRequest,
    db: Session = Depends(get_db)
):
    #disease prediction
    disease_result = predict_disease(
    request.symptoms
    )

    predicted_disease = disease_result[
        "predicted_disease"
    ]

    #treatment recommendation
    treatment_result = get_best_treatment(
    predicted_disease,
    db
    )

    if treatment_result is None:
        return {
            "error": "Disease not found"
        }

    recommended_treatment = treatment_result[
        "recommended_treatment"
    ]

    #determine severity (basic rule)
    if predicted_disease == "Flu":
        severity = "Mild"
    else:
        severity = "Moderate"
    
    #recovery prediction
    recovery_result = predict_recovery(
    predicted_disease,
    severity,
    recommended_treatment,
    request.age
    )

    #complication prediction
    complication_result = predict_complication(
    predicted_disease,
    severity,
    recommended_treatment,
    request.age
    )

    summary = (
    f"The patient is predicted to have "
    f"{predicted_disease} "
    f"with {disease_result['confidence']}% confidence. "
    f"The recommended treatment is "
    f"{recommended_treatment} "
    f"with a historical success rate of "
    f"{treatment_result['success_rate']}%. "
    f"Expected recovery time is "
    f"{recovery_result['expected_recovery_days']} days. "
    f"Complication risk is "
    f"{complication_result['risk_level']} "
    f"({complication_result['probability_of_complication']}% probability)."
    )

    #return everything
    return {
    "disease_prediction": disease_result,
    "treatment_recommendation": treatment_result,
    "recovery_prediction": recovery_result,
    "complication_prediction": complication_result,
    "clinical_summary": summary
    }






