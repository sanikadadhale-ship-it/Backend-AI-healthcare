from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    message: str
    report_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    sender: str
    text: str
    timestamp: str
    suggested_actions: Optional[List[str]] = []
    medical_disclaimer: bool = True

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime

class ChatSessionDetailResponse(BaseModel):
    id: str
    title: str
    messages: List[ChatMessageResponse]
    created_at: datetime
