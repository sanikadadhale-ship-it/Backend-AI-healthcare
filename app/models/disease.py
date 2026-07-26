from typing import Optional, List
from pydantic import BaseModel, Field

class DiseaseModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    category: str
    overview: str
    symptoms: List[str] = []
    causes: List[str] = []
    risk_factors: List[str] = []
    prevention: List[str] = []
    treatment_options: List[str] = []
    when_to_see_doctor: Optional[str] = None

    class Config:
        populate_by_name = True
