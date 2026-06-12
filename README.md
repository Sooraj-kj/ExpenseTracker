# ExpenseTracker

A personal expense tracker web app built with **FastAPI** (Python) + **SQLite** + **Vanilla HTML/JS**.

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

> Interactive API docs available at `http://localhost:8000/docs`

---

## Stack & Tradeoffs

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI (Python) | Fast to write, auto-generates API docs, built-in Pydantic validation |
| Database | SQLite via SQLAlchemy | Zero setup, file-based, perfect for local single-user use |
| Frontend | Vanilla HTML/JS | No build step, no dependencies, loads instantly |

---

## Features

- **Add expense** — title, amount, category, date (defaults to today), optional note
- **View all expenses** — sorted by date descending, all fields shown
- **Edit & delete** — modal edit form, confirmation on delete
- **Monthly summary** — total spent, top category, daily average, category bar chart, month navigation
- **Filters** — by category, date range (from/to), title partial match (debounced)

---

## Project Structure

```
ExpenseTracker/
├── backend/
│   ├── main.py          # FastAPI app + route definitions
│   ├── database.py      # SQLAlchemy engine + Expense model
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Database operations
│   └── requirements.txt
├── frontend/
│   └── index.html       # Single-file UI (HTML + CSS + JS)
└── README.md
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/expenses` | List expenses (filterable by category, date range, title) |
| POST | `/api/expenses` | Create a new expense |
| GET | `/api/expenses/{id}` | Get a single expense |
| PUT | `/api/expenses/{id}` | Update an expense |
| DELETE | `/api/expenses/{id}` | Delete an expense |
| GET | `/api/summary/monthly` | Monthly summary with category breakdown |
| GET | `/api/categories` | List valid categories |

**Filter query params for `GET /api/expenses`:**

| Param | Type | Example |
|---|---|---|
| `category` | string | `?category=Food` |
| `date_from` | date | `?date_from=2026-06-01` |
| `date_to` | date | `?date_to=2026-06-30` |
| `title` | string | `?title=coffee` (partial match) |

---

## What's Done vs Skipped

**Done**
- All 5 spec requirements fully implemented
- Client-side + server-side input validation
- Empty states for no results
- Pydantic v2 compatible schemas

**Skipped**
- Multi-currency (not required per spec)
- Authentication / multi-user support
- Test suite
- Deployment config
- Pagination (200 result cap — adequate for personal use)

---

## Known Rough Edges

- No undo after delete
- Note field is truncated in the list view — full text visible in the Edit modal
- Date range filter is inclusive on both ends; if `date_from > date_to` the query returns empty gracefully