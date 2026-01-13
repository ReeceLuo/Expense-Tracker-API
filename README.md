# Expense Tracker API

A RESTful API for tracking personal expenses built with FastAPI and PostgreSQL.

## Features

- User management (create, read, update, delete)
- Expense tracking with paid/unpaid status
- User financial summaries with budget tracking
- Expense categorization
- PostgreSQL database with SQLAlchemy ORM

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd ExpenseTrackerAPI
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables

Create a `.env` file in the project root:
```
database_url=postgresql://expense_tracker_user:expense_tracker_api@localhost:5432/expense_tracker_db
```

For SQLite (development):
```
database_url=sqlite:///./expense_tracker.db
```

5. Set up PostgreSQL database (if using PostgreSQL)
```sql
CREATE USER expense_tracker_user WITH PASSWORD 'expense_tracker_api';
CREATE DATABASE expense_tracker_db OWNER expense_tracker_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO expense_tracker_user;
```

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get user details
- `GET /users/{user_id}/summary` - Get user financial summary
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Expenses
- `POST /expenses/` - Create a new expense
- `GET /expenses/{expense_id}` - Get expense details
- `GET /expenses/user/{user_id}` - Get all expenses for a user
- `PUT /expenses/{expense_id}` - Update expense
- `PATCH /expenses/{expense_id}/toggle-paid` - Toggle expense paid status
- `DELETE /expenses/{expense_id}` - Delete expense

## Project Structure

```
ExpenseTrackerAPI/
├── routes/
│   ├── UserRoutes.py      # User endpoint handlers
│   └── ExpenseRoutes.py   # Expense endpoint handlers
├── config.py              # Database configuration
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic validation schemas
├── main.py                # FastAPI application entry point
├── requirements.txt       # Project dependencies
└── .env                   # Environment variables (create this)
```
