from pydantic import BaseModel
from typing import Optional
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str

class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    user_id: int

class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True