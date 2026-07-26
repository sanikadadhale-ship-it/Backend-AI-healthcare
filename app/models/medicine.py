from typing import Optional, List
from pydantic import BaseModel, Field

class MedicineModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    brand_names: List[str] = []
    category: str
    dosage_form: str  # Tablet, Syrup, Injection, etc.
    strength: str
    uses: List[str] = []
    side_effects: List[str] = []
    precautions: List[str] = []
    manufacturer: Optional[str] = None
    requires_prescription: bool = True

    class Config:
        populate_by_name = True
