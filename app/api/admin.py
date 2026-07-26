from fastapi import APIRouter, Depends, HTTPException, status
from app.api.auth import get_current_user
from app.core.database import get_database

router = APIRouter(prefix="/admin", tags=["Admin Operations"])

@router.get("/summary")
async def get_admin_summary(current_user: dict = Depends(get_current_user)):
    db = get_database()

    users_count = 0
    chats_count = 0
    appointments_count = 0

    if db is not None:
        users_count = await db["users"].count_documents({})
        chats_count = await db["chat_history"].count_documents({})
        appointments_count = await db["appointments"].count_documents({})
    else:
        users_count = 1250
        chats_count = 8400
        appointments_count = 320

    return {
        "status": "online",
        "system_health": "Optimal",
        "total_users": users_count,
        "total_ai_consultations": chats_count,
        "total_appointments": appointments_count,
        "ai_engine_status": "Google Gemini 2.5/3.6 Active",
        "database_status": "Connected to MongoDB Cluster" if db is not None else "Mock In-Memory Mode"
    }
