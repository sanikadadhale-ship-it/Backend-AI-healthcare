from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AppointmentModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    doctor_name: str
    specialty: str
    appointment_date: datetime
    location_or_link: str
    status: str = "scheduled"  # "scheduled" | "completed" | "cancelled"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
