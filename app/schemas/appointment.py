from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    doctor_name: str
    specialty: str
    appointment_date: datetime
    location_or_link: str
    notes: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: str
    user_id: str
    doctor_name: str
    specialty: str
    appointment_date: datetime
    location_or_link: str
    status: str
    notes: Optional[str]
    created_at: datetime
