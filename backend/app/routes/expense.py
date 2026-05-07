from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.expense_service import create_expense, get_expenses
from app.config.database import get_db

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def add_expense(expense: ExpenseCreate, db:Session = Depends(get_db)):
    return create_expense(db, user_id=3, data=expense)

@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(db: Session = Depends(get_db)):
    return get_expenses(db, user_id=3)