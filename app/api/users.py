from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.api.auth import get_current_user
from app.core.database import get_database
from app.schemas.user import UserResponse, UserUpdate
from app.services.db_service import fix_object_id

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user.get("id", current_user.get("_id", "demo_id"))),
        "email": current_user.get("email", "patient@medimind.ai"),
        "full_name": current_user.get("full_name", "Alex Morgan"),
        "phone": current_user.get("phone", "+1 555-0192"),
        "age": current_user.get("age", 34),
        "gender": current_user.get("gender", "Male"),
        "blood_group": current_user.get("blood_group", "O+"),
        "allergies": current_user.get("allergies", ["Penicillin"]),
        "chronic_conditions": current_user.get("chronic_conditions", ["Mild Hypertension"]),
        "avatar": current_user.get("avatar", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"),
        "is_admin": current_user.get("is_admin", False),
        "created_at": current_user.get("created_at", "2026-01-01T00:00:00")
    }

@router.put("/me", response_model=UserResponse)
async def update_user_me(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = str(current_user.get("id", current_user.get("_id", "")))

    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    
    if db is not None and user_id and user_id != "demo_id":
        await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        updated_doc = await db["users"].find_one({"_id": ObjectId(user_id)})
        return fix_object_id(updated_doc)

    # In-memory return fallback
    merged = {**current_user, **update_data}
    return {
        "id": user_id or "demo_id",
        "email": merged.get("email", "patient@medimind.ai"),
        "full_name": merged.get("full_name", "Alex Morgan"),
        "phone": merged.get("phone"),
        "age": merged.get("age"),
        "gender": merged.get("gender"),
        "blood_group": merged.get("blood_group", "O+"),
        "allergies": merged.get("allergies", []),
        "chronic_conditions": merged.get("chronic_conditions", []),
        "avatar": merged.get("avatar"),
        "is_admin": merged.get("is_admin", False),
        "created_at": merged.get("created_at", "2026-01-01T00:00:00")
    }
