# ExpenseTracker

A personal expense tracker web app built with **FastAPI** (Python) + **SQLite** + ** HTML/JS**.

## How to Run

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --reload --port 8000

# 3. Open in browser
# http://localhost:8000
```

The SQLite database (`expenses.db`) is created automatically in the `backend/` directory on first run.

---

## Stack & Tradeoffs

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI (Python) | Fast to write, auto-generates API docs at `/docs`, built-in validation |
| Database | SQLite via SQLAlchemy | Zero setup, file-based, perfect for local use |
| Frontend | Vanilla HTML/JS | No build step, no dependencies, loads instantly |


## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/expenses` | List expenses (filterable) |
| POST | `/api/expenses` | Create expense |
| GET | `/api/expenses/{id}` | Get single expense |
| PUT | `/api/expenses/{id}` | Update expense |
| DELETE | `/api/expenses/{id}` | Delete expense |
| GET | `/api/summary/monthly` | Monthly summary |
| GET | `/api/categories` | List valid categories |