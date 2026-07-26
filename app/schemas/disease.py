from typing import Optional, List
from pydantic import BaseModel

class DiseaseCreate(BaseModel):
    name: str
    category: str
    overview: str
    symptoms: List[str] = []
    causes: List[str] = []
    risk_factors: List[str] = []
    prevention: List[str] = []
    treatment_options: List[str] = []
    when_to_see_doctor: Optional[str] = None

class DiseaseResponse(BaseModel):
    id: str
    name: str
    category: str
    overview: str
    symptoms: List[str]
    causes: List[str]
    risk_factors: List[str]
    prevention: List[str]
    treatment_options: List[str]
    when_to_see_doctor: Optional[str]
