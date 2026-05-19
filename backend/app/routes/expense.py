from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate, ExpenseListResponse
from app.services.expense_service import create_expense, get_expenses, get_expense_by_expense_id, delete_expense, update_expense_by_id
from app.config.database import get_db
from app.utils.dependency import get_current_user
from app.models.user import User
from fastapi import HTTPException, Query

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    return create_expense(db, user_id=current_user.id, expense_data=expense)

@router.get("/", response_model=ExpenseListResponse)
def list_expenses(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    return get_expenses(
        db = db,
        user_id=current_user.id,
        limit=limit,
        offset=offset,
        category=category,
        search=search
    )

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    expense = get_expense_by_expense_id(db, expense_id, current_user.id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
   
    return expense

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense_route(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    expense = get_expense_by_expense_id(db, expense_id, current_user.id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    

    updated_expense = update_expense_by_id(db, expense, expense_data)

    return updated_expense


@router.delete("/{expense_id}")
def delete_expense_route(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    expense = get_expense_by_expense_id(db, expense_id, current_user.id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    

    return delete_expense(db, expense)