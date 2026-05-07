from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.expense_service import create_expense, get_expenses
from app.config.database import get_db
from app.utils.dependency import get_current_user
from app.models.user import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate, 
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)):
    
    return create_expense(db, user_id=get_current_user.id, data=expense)

@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)):
    
    return get_expenses(db, user_id=get_current_user.id)