from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, LoginRequest
from app.config.database import get_db
from app.services.user_service import create_user, get_user_by_email, authenticate_user
from app.utils.auth import create_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user =  create_user(db, user.email, user.password)
    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return new_user

@router.get("/", response_model=UserResponse)
def read_user(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentails")
    
    token = create_token({"user_id": db_user.id})
    return {
        "access_token": token,
        "token_type": "bearer"
    }