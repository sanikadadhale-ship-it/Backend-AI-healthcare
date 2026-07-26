from typing import List, Optional
from fastapi import APIRouter, Query
from app.core.database import get_database
from app.schemas.disease import DiseaseResponse
from app.services.db_service import fix_object_id

router = APIRouter(prefix="/disease", tags=["Disease & Clinical Information"])

MOCK_DISEASES = [
    {
        "id": "dis_01",
        "name": "Essential Hypertension",
        "category": "Cardiovascular",
        "overview": "A chronic medical condition in which blood pressure in the arteries is persistently elevated.",
        "symptoms": ["Frequent morning headaches", "Shortness of breath", "Occasional nosebleeds", "Dizziness"],
        "causes": ["Genetics", "High dietary sodium intake", "Sedentary lifestyle", "Stress"],
        "risk_factors": ["Age > 45", "Family history", "Overweight", "Tobacco use"],
        "prevention": ["DASH Diet low in sodium", "30 minutes daily aerobic exercise", "Stress reduction"],
        "treatment_options": ["ACE Inhibitors", "Calcium Channel Blockers (Amlodipine)", "Lifestyle changes"],
        "when_to_see_doctor": "If blood pressure reading exceeds 180/120 mmHg or accompanies chest pressure."
    },
    {
        "id": "dis_02",
        "name": "Type 2 Diabetes Mellitus",
        "category": "Endocrine & Metabolic",
        "overview": "A long-term metabolic disorder characterized by high blood sugar, insulin resistance, and relative lack of insulin.",
        "symptoms": ["Increased thirst (Polydipsia)", "Frequent urination (Polyuria)", "Fatigue", "Blurred vision"],
        "causes": ["Pancreatic beta-cell dysfunction", "Insulin receptor insensitivity"],
        "risk_factors": ["BMI > 25", "Physical inactivity", "High carbohydrate diet"],
        "prevention": ["Balanced glycemic diet", "Regular exercise", "Weight management"],
        "treatment_options": ["Metformin", "SGLT2 inhibitors", "Insulin therapy when indicated"],
        "when_to_see_doctor": "Fasting blood glucose consistently exceeding 126 mg/dL."
    }
]

@router.get("/search", response_model=List[DiseaseResponse])
async def search_disease(q: Optional[str] = Query(None, description="Disease name or symptom search")):
    db = get_database()
    if db is not None:
        query = {}
        if q:
            query = {
                "$or": [
                    {"name": {"$regex": q, "$options": "i"}},
                    {"symptoms": {"$regex": q, "$options": "i"}},
                    {"category": {"$regex": q, "$options": "i"}}
                ]
            }
        cursor = db["diseases"].find(query)
        docs = await cursor.to_list(length=50)
        if docs:
            return [fix_object_id(d) for d in docs]

    if q:
        q_lower = q.lower()
        return [
            d for d in MOCK_DISEASES
            if q_lower in d["name"].lower()
            or any(q_lower in s.lower() for s in d["symptoms"])
            or q_lower in d["category"].lower()
        ]
    return MOCK_DISEASES
