from sqlalchemy import Column, Integer, String, Date
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    hospital = Column(String)
    age = Column(Integer)
    gender = Column(String)

    symptoms = Column(String)
    disease = Column(String)

    treatment = Column(String)
    outcome = Column(String)

    visit_date = Column(Date)