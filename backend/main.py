from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
import os

from database import get_db
from schemas import ExpenseCreate, ExpenseUpdate, ExpenseOut, MonthlySummary, VALID_CATEGORIES
import crud

app = FastAPI(title="Expense Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
def read_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))


# ── Expenses CRUD ──────────────────────────────────────────────────────────────

@app.get("/api/expenses", response_model=List[ExpenseOut])
def list_expenses(
    category: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    title: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return crud.get_expenses(db, category=category, date_from=date_from, date_to=date_to, title=title)


@app.post("/api/expenses", response_model=ExpenseOut, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


@app.get("/api/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense(db, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.put("/api/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_expense(db, expense_id, expense)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated


@app.delete("/api/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_expense(db, expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")


# ── Summary ────────────────────────────────────────────────────────────────────

@app.get("/api/summary/monthly")
def monthly_summary(
    year: int = Query(default=date.today().year),
    month: int = Query(default=date.today().month, ge=1, le=12),
    db: Session = Depends(get_db),
):
    return crud.get_monthly_summary(db, year, month)


@app.get("/api/categories")
def get_categories():
    return {"categories": VALID_CATEGORIES}