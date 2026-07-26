from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class ChatMessageModel(BaseModel):
    sender: str  # "user" | "ai"
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    medical_disclaimer: bool = True
    suggested_actions: Optional[List[str]] = []

class ChatSessionModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    title: str = "Clinical AI Consultation"
    messages: List[ChatMessageModel] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
