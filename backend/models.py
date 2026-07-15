from sqlalchemy import Column, Integer, String, Date
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    hospital = Column(String)
    district = Column(String)          # NEW

    age = Column(Integer)
    gender = Column(String)
    occupation = Column(String)        # NEW

    symptoms = Column(String)
    severity = Column(String)          # NEW
    symptom_duration = Column(Integer) # NEW

    disease = Column(String)

    treatment = Column(String)

    outcome = Column(String)
    recovery_days = Column(Integer)    # NEW
    complications = Column(String)     # NEW

    visit_date = Column(Date)