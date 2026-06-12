# ExpenseTracker

A personal expense tracker web app built with **FastAPI** (Python) + **SQLite** + **vanilla HTML/JS**.

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

**Tradeoffs made:**
- SQLite is single-writer; fine for a personal app, not for multi-user production.
- Vanilla JS keeps things simple but means no component reuse — a larger app would benefit from React/Vue.
- No authentication (not required per spec).

---

## What's Done

- ✅ Add expense (title, amount, category, date, note)
- ✅ View all expenses sorted by date (most recent first)
- ✅ Edit any expense (inline modal)
- ✅ Delete any expense (with confirmation)
- ✅ Monthly summary — total, top category, daily average, breakdown bar chart
- ✅ Navigate between months in summary view
- ✅ Filter by category, date range (from/to), title (partial match, debounced)
- ✅ Input validation (client + server side)
- ✅ Empty states for no results
- ✅ Auto-docs at `/docs` (Swagger UI) and `/redoc`

## What's Skipped

- ❌ Multi-currency (spec said not required)
- ❌ Authentication / multi-user
- ❌ Test suite
- ❌ Deployment config
- ❌ Pagination (limit of 200 results applied; adequate for personal use)

## Known Rough Edges

- Deleting an expense while a filter is active re-applies the filter correctly, but the deleted row disappears immediately (no undo).
- Date range filter is inclusive on both ends.
- The `note` field in the expense list is truncated with ellipsis — full note is visible in the Edit modal.

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