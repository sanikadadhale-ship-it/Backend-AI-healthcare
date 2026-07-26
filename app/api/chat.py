from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from app.api.auth import get_current_user
from app.core.database import get_database
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionResponse,
    ChatSessionDetailResponse
)
from app.services.ai_service import ai_service
from app.services.db_service import fix_object_id

router = APIRouter(prefix="/chat", tags=["AI Clinical Chat"])

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = str(current_user.get("id", current_user.get("_id", "demo_id")))

    if db is not None:
        cursor = db["chat_history"].find({"user_id": user_id}).sort("updated_at", -1)
        sessions = await cursor.to_list(length=100)
        res = []
        for s in sessions:
            res.append({
                "id": str(s["_id"]),
                "title": s.get("title", "Clinical Session"),
                "message_count": len(s.get("messages", [])),
                "created_at": s.get("created_at", datetime.utcnow()),
                "updated_at": s.get("updated_at", datetime.utcnow())
            })
        return res

    # Mock fallback
    return [
        {
            "id": "session_001",
            "title": "Blood Pressure & Lipid Panel Analysis",
            "message_count": 4,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]

@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    chat_input: ChatMessageCreate,
    session_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("id", current_user.get("_id", "demo_id")))
    db = get_database()

    # Get clinical AI response using Gemini or clinical rules engine
    ai_text = await ai_service.generate_clinical_response(chat_input.message)

    ai_msg = {
        "sender": "ai",
        "text": ai_text,
        "timestamp": datetime.utcnow().strftime("%H:%M:%S"),
        "suggested_actions": [
            "Explain lipid panel ranges",
            "Dietary advice for 120/78 mmHg",
            "Check side effects of Amlodipine"
        ],
        "medical_disclaimer": True
    }

    if db is not None:
        user_msg = {
            "sender": "user",
            "text": chat_input.message,
            "timestamp": datetime.utcnow().strftime("%H:%M:%S")
        }

        if session_id and ObjectId.is_valid(session_id):
            await db["chat_history"].update_one(
                {"_id": ObjectId(session_id), "user_id": user_id},
                {
                    "$push": {"messages": {"$each": [user_msg, ai_msg]}},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
        else:
            new_session = {
                "user_id": user_id,
                "title": chat_input.message[:40] + "...",
                "messages": [user_msg, ai_msg],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            await db["chat_history"].insert_one(new_session)

    return ai_msg

@router.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(session_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = str(current_user.get("id", current_user.get("_id", "demo_id")))

    if db is not None and ObjectId.is_valid(session_id):
        await db["chat_history"].delete_one({"_id": ObjectId(session_id), "user_id": user_id})

    return None
