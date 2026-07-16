from pydantic import BaseModel
from datetime import date

class PatientResponse(BaseModel):
    id: int
    hospital: str
    age: int
    gender: str
    symptoms: str
    disease: str
    treatment: str
    outcome: str
    visit_date: date

    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    symptoms: str

class TreatmentRequest(BaseModel):
    disease: str

class RecoveryRequest(BaseModel):
    disease: str
    severity: str
    treatment: str
    age: int

class ComplicationRequest(BaseModel):
    disease: str
    severity: str
    treatment: str
    age: int