from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NotificationModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    title: str
    message: str
    type: str = "general"  # "medication" | "lab_report" | "appointment" | "general"
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
