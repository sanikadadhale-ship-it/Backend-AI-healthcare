from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from app.api.auth import get_current_user
from app.core.database import get_database
from app.schemas.notification import NotificationResponse, NotificationCreate
from app.services.db_service import fix_object_id

router = APIRouter(prefix="/notification", tags=["Notifications"])

@router.get("/list", response_model=List[NotificationResponse])
async def list_notifications(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("id", current_user.get("_id", "demo_id")))
    db = get_database()

    if db is not None:
        cursor = db["notifications"].find({"user_id": user_id}).sort("created_at", -1)
        notes = await cursor.to_list(length=100)
        return [fix_object_id(n) for n in notes]

    # Mock list
    return [
        {
            "id": "notif_01",
            "user_id": user_id,
            "title": "Medication Reminder 💊",
            "message": "Take Amlodipine 5mg with water at 09:00 AM",
            "type": "medication",
            "is_read": False,
            "created_at": datetime.utcnow()
        },
        {
            "id": "notif_02",
            "user_id": user_id,
            "title": "Lab Report Ingested 🩸",
            "message": "Lipid panel analysis completed. Heart health score: 94/100",
            "type": "lab_report",
            "is_read": True,
            "created_at": datetime.utcnow()
        }
    ]

@router.put("/mark-read/{notification_id}", status_code=status.HTTP_200_OK)
async def mark_as_read(notification_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("id", current_user.get("_id", "demo_id")))
    db = get_database()

    if db is not None and ObjectId.is_valid(notification_id):
        await db["notifications"].update_one(
            {"_id": ObjectId(notification_id), "user_id": user_id},
            {"$set": {"is_read": True}}
        )

    return {"status": "success", "message": "Notification marked as read"}
