from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate

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


def get_expenses(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()

def get_expense_by_expense_id(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

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