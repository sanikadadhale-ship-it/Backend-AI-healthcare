from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from bson import ObjectId
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from app.core.database import get_database
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.models.user import UserModel
from app.services.db_service import fix_object_id

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    db = get_database()
    if db is None:
        # Mock mode if database not yet connected
        return {
            "id": user_id,
            "email": "user@medimind.ai",
            "full_name": "Demo Patient",
            "is_admin": False
        }

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception
    return fix_object_id(user)

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    db = get_database()
    if db is not None:
        existing = await db["users"].find_one({"email": user_in.email})
        if existing:
            raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_pw = get_password_hash(user_in.password)
    user_dict = {
        "email": user_in.email,
        "hashed_password": hashed_pw,
        "full_name": user_in.full_name,
        "phone": user_in.phone,
        "allergies": [],
        "chronic_conditions": [],
        "is_active": True,
        "is_admin": False
    }

    user_id = "demo_user_id"
    if db is not None:
        res = await db["users"].insert_one(user_dict)
        user_id = str(res.inserted_id)

    access_token = create_access_token(subject=user_id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "email": user_in.email,
        "full_name": user_in.full_name
    }

@router.post("/login", response_model=Token)
async def login(user_in: UserLogin):
    db = get_database()
    user = None
    if db is not None:
        user = await db["users"].find_one({"email": user_in.email})

    if not user:
        # Check mock fallback
        if user_in.email == "demo@medimind.ai" and user_in.password == "password":
            token = create_access_token(subject="demo_user_123")
            return {
                "access_token": token,
                "token_type": "bearer",
                "user_id": "demo_user_123",
                "email": user_in.email,
                "full_name": "Demo Patient"
            }
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    user_id = str(user["_id"])
    access_token = create_access_token(subject=user_id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "email": user["email"],
        "full_name": user["full_name"]
    }
