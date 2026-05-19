from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate
from sqlalchemy import or_

def create_expense(db: Session, user_id: int, expense_data: ExpenseCreate):
    expense = Expense(
        title = expense_data.title,
        amount = expense_data.amount,
        category = expense_data.category,
        user_id = user_id
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses(
    db: Session,
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    category: str | None = None,
    search: str | None = None
    ):

    # return only user specific records
    query = db.query(Expense).filter(Expense.user_id == user_id)

    # search by category
    if category:
        query = query.filter(Expense.category == category)
    
    # search by title
    if search:
        query = query.filter(
        or_(
            Expense.title.ilike(f"%{search}%"),
            Expense.category.ilike(f"%{search}%")
        )
    )
    total = query.count()
    # pagination
    data =  query.offset(offset).limit(limit).all()
    
    return {
        "total_items": total,
        "data": data
        }

def get_expense_by_expense_id(db: Session, expense_id: int, user_id: int):
    return db.query(Expense).filter(
        Expense.id == expense_id, 
        Expense.user_id ==user_id
        ).first()

def update_expense_by_id(db: Session, expense, update_data):
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, expense):
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}