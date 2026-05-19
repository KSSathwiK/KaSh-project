from pydantic import BaseModel, Field
from typing import Optional

class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=2, max_length=50)

class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    user_id: int

    class Config:
        from_attributes = True

class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=2, max_length=50)

class ExpenseListResponse(BaseModel):
    total_items: int
    data: list[ExpenseResponse]

    