from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.config.database import get_db
from app.services.user_service import create_user, get_user_by_email

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