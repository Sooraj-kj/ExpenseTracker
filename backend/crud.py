from sqlalchemy.orm import Session
from sqlalchemy import extract
from database import Expense
from schemas import ExpenseCreate, ExpenseUpdate
from datetime import date as date_type
from typing import Optional


def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()


def get_expenses(
    db: Session,
    category: Optional[str] = None,
    date_from: Optional[date_type] = None,
    date_to: Optional[date_type] = None,
    title: Optional[str] = None,
    skip: int = 0,
    limit: int = 200,
):
    q = db.query(Expense)
    if category:
        q = q.filter(Expense.category == category)
    if date_from:
        q = q.filter(Expense.date >= date_from)
    if date_to:
        q = q.filter(Expense.date <= date_to)
    if title:
        q = q.filter(Expense.title.ilike(f"%{title}%"))
    return q.order_by(Expense.date.desc(), Expense.id.desc()).offset(skip).limit(limit).all()


def create_expense(db: Session, expense: ExpenseCreate):
    data = expense.model_dump(by_alias=False)
    # rename expense_date -> date for the ORM
    data["date"] = data.pop("expense_date")
    db_expense = Expense(**data)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(db: Session, expense_id: int, expense: ExpenseUpdate):
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return None
    update_data = expense.model_dump(by_alias=False, exclude_unset=True)
    if "expense_date" in update_data:
        update_data["date"] = update_data.pop("expense_date")
    for key, value in update_data.items():
        setattr(db_expense, key, value)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int):
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return False
    db.delete(db_expense)
    db.commit()
    return True


def get_monthly_summary(db: Session, year: int, month: int):
    expenses = (
        db.query(Expense)
        .filter(
            extract("year", Expense.date) == year,
            extract("month", Expense.date) == month,
        )
        .all()
    )
    total = sum(e.amount for e in expenses)
    by_category = {}
    for e in expenses:
        by_category[e.category] = round(by_category.get(e.category, 0) + e.amount, 2)
    return {
        "month": f"{year}-{month:02d}",
        "total": round(total, 2),
        "by_category": by_category,
        "expense_count": len(expenses),
    }