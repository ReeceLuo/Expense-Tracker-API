# Expense Tracker API

A RESTful API for tracking personal expenses built with FastAPI and PostgreSQL. Made w/o AI (except README.md lol)

## Features

- **JWT Authentication** - Secure token-based authentication with bcrypt password hashing
- User management (create, read, update, delete)
- Expense tracking with paid/unpaid status
- User financial summaries with budget tracking
- Expense categorization
- PostgreSQL database with SQLAlchemy ORM
- Protected endpoints with authorization checks

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **python-jose** - JWT token handling
- **passlib + bcrypt** - Password hashing

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
SECRET_KEY=your-secret-key-here
```

For SQLite (development):
```
database_url=sqlite:///./expense_tracker.db
SECRET_KEY=your-secret-key-here
```

Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
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

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token

### Users (Protected - requires Bearer token)
- `GET /users/me` - Get current user details
- `GET /users/me/summary` - Get current user financial summary
- `PUT /users/me` - Update current user
- `DELETE /users/me` - Delete current user

### Expenses (Protected - requires Bearer token)
- `POST /expenses/` - Create a new expense
- `GET /expenses/{expense_id}` - Get expense details (own expenses only)
- `GET /expenses/user` - Get all expenses for current user
- `PUT /expenses/{expense_id}` - Update expense (own expenses only)
- `PATCH /expenses/{expense_id}/toggle-paid` - Toggle expense paid status
- `DELETE /expenses/{expense_id}` - Delete expense (own expenses only)

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. Register a new user at `POST /auth/register`
2. Login at `POST /auth/login` to receive an access token
3. Include the token in the `Authorization` header for protected requests:
   ```
   Authorization: Bearer <your-access-token>
   ```

Tokens expire after 30 minutes.

## Project Structure

```
ExpenseTrackerAPI/
├── routes/
│   ├── __init__.py        # Package initialization
│   ├── AuthRoutes.py      # Authentication endpoints
│   ├── UserRoutes.py      # User endpoint handlers
│   └── ExpenseRoutes.py   # Expense endpoint handlers
├── auth.py                # JWT authentication utilities
├── config.py              # Database configuration
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic validation schemas
├── main.py                # FastAPI application entry point
├── requirements.txt       # Project dependencies
└── .env                   # Environment variables (create this)
```
