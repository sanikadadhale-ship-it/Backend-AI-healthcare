from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.core.database import get_database
from app.schemas.medicine import MedicineResponse, MedicineCreate
from app.services.db_service import fix_object_id

router = APIRouter(prefix="/medicine", tags=["Medicine Knowledge Base"])

MOCK_MEDICINES = [
    {
        "id": "med_01",
        "name": "Amlodipine Besylate",
        "brand_names": ["Norvasc", "Amlopress", "Amlovas"],
        "category": "Antihypertensive / Calcium Channel Blocker",
        "dosage_form": "Tablet",
        "strength": "5mg / 10mg",
        "uses": ["Hypertension (High Blood Pressure)", "Coronary Artery Disease", "Angina"],
        "side_effects": ["Swelling of ankles/feet (Edema)", "Dizziness", "Flushing"],
        "precautions": ["Avoid grapefruit juice", "Regular blood pressure monitoring"],
        "manufacturer": "Pfizer / Generic",
        "requires_prescription": True
    },
    {
        "id": "med_02",
        "name": "Metformin Hydrochloride",
        "brand_names": ["Glucophage", "Glycomet"],
        "category": "Antidiabetic / Biguanide",
        "dosage_form": "Tablet",
        "strength": "500mg / 850mg / 1000mg",
        "uses": ["Type 2 Diabetes Mellitus", "Insulin Resistance"],
        "side_effects": ["Nausea", "Mild stomach upset", "Metallic taste"],
        "precautions": ["Take with meals", "Monitor renal function regularly"],
        "manufacturer": "Merck",
        "requires_prescription": True
    },
    {
        "id": "med_03",
        "name": "Atorvastatin Calcium",
        "brand_names": ["Lipitor", "Atorva"],
        "category": "Statin / Lipid-Lowering Agent",
        "dosage_form": "Tablet",
        "strength": "10mg / 20mg / 40mg",
        "uses": ["Hypercholesterolemia (High LDL)", "Cardiovascular Event Prevention"],
        "side_effects": ["Mild muscle stiffness", "Digestive changes"],
        "precautions": ["Take at bedtime", "Periodic liver function testing"],
        "manufacturer": "Pfizer / Viatris",
        "requires_prescription": True
    }
]

@router.get("/search", response_model=List[MedicineResponse])
async def search_medicine(q: Optional[str] = Query(None, description="Medicine or active ingredient query")):
    db = get_database()
    if db is not None:
        query = {}
        if q:
            query = {
                "$or": [
                    {"name": {"$regex": q, "$options": "i"}},
                    {"brand_names": {"$regex": q, "$options": "i"}},
                    {"category": {"$regex": q, "$options": "i"}}
                ]
            }
        cursor = db["medicine"].find(query)
        results = await cursor.to_list(length=50)
        if results:
            return [fix_object_id(r) for r in results]

    if q:
        q_lower = q.lower()
        return [
            m for m in MOCK_MEDICINES
            if q_lower in m["name"].lower()
            or any(q_lower in b.lower() for b in m["brand_names"])
            or q_lower in m["category"].lower()
        ]
    return MOCK_MEDICINES
