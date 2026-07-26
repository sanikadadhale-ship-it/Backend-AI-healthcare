from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from app.api.auth import get_current_user
from app.core.database import get_database
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services.db_service import fix_object_id

router = APIRouter(prefix="/appointment", tags=["Appointments & Scheduling"])

@router.get("/list", response_model=List[AppointmentResponse])
async def list_appointments(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("id", current_user.get("_id", "demo_id")))
    db = get_database()

    if db is not None:
        cursor = db["appointments"].find({"user_id": user_id}).sort("appointment_date", 1)
        apps = await cursor.to_list(length=100)
        return [fix_object_id(a) for a in apps]

    # Mock list
    return [
        {
            "id": "app_1",
            "user_id": user_id,
            "doctor_name": "Dr. Sarah Jenkins, MD",
            "specialty": "Cardiology & Vascular Medicine",
            "appointment_date": datetime.utcnow() + timedelta(days=3),
            "location_or_link": "Metropolitan Health Tower / Telehealth Room 4",
            "status": "scheduled",
            "notes": "Follow up on blood pressure trend & lipid panel",
            "created_at": datetime.utcnow()
        }
    ]

@router.post("/create", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(app_in: AppointmentCreate, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("id", current_user.get("_id", "demo_id")))
    db = get_database()

    doc = {
        "user_id": user_id,
        "doctor_name": app_in.doctor_name,
        "specialty": app_in.specialty,
        "appointment_date": app_in.appointment_date,
        "location_or_link": app_in.location_or_link,
        "status": "scheduled",
        "notes": app_in.notes,
        "created_at": datetime.utcnow()
    }

    if db is not None:
        res = await db["appointments"].insert_one(doc)
        doc["_id"] = res.inserted_id
        return fix_object_id(doc)

    doc["id"] = "app_new_123"
    return doc
