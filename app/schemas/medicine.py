from typing import Optional, List
from pydantic import BaseModel

class MedicineCreate(BaseModel):
    name: str
    brand_names: List[str] = []
    category: str
    dosage_form: str
    strength: str
    uses: List[str] = []
    side_effects: List[str] = []
    precautions: List[str] = []
    manufacturer: Optional[str] = None
    requires_prescription: bool = True

class MedicineResponse(BaseModel):
    id: str
    name: str
    brand_names: List[str]
    category: str
    dosage_form: str
    strength: str
    uses: List[str]
    side_effects: List[str]
    precautions: List[str]
    manufacturer: Optional[str]
    requires_prescription: bool
