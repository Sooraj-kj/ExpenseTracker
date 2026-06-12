from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date as date_type


VALID_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]


class ExpenseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    category: str
    expense_date: date_type = Field(default_factory=date_type.today, alias="date")
    note: Optional[str] = None

    model_config = {"populate_by_name": True}

    @field_validator("category")
    @classmethod
    def category_must_be_valid(cls, v):
        if v not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")
        return v

    @field_validator("amount")
    @classmethod
    def round_amount(cls, v):
        return round(v, 2)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    expense_date: Optional[date_type] = Field(None, alias="date")
    note: Optional[str] = None

    model_config = {"populate_by_name": True}

    @field_validator("category")
    @classmethod
    def category_must_be_valid(cls, v):
        if v is not None and v not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")
        return v


class ExpenseOut(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    date: date_type
    note: Optional[str] = None

    model_config = {"from_attributes": True}


class MonthlySummary(BaseModel):
    month: str
    total: float
    by_category: dict
    expense_count: int