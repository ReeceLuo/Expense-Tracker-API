# Expense Tracker API

A RESTful API for tracking personal expenses built with FastAPI and PostgreSQL.

## Features

- **JWT Authentication** - Secure token-based authentication with bcrypt password hashing
- User management (create, read, update, delete)
- Expense tracking with paid/unpaid status
- User financial summaries with budget tracking
- Expense categorization
- PostgreSQL database with SQLAlchemy ORM
- Protected endpoints with authorization checks
- **Redis Caching** - Response caching for expensive queries (user summaries)
- **Rate Limiting** - Protection against abuse on authentication endpoints

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **Redis** - In-memory caching and rate limiting
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **python-jose** - JWT token handling
- **bcrypt** - Password hashing

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
redis_url=redis://localhost:6379/0
redis_enabled=true
```

For SQLite (development):
```
database_url=sqlite:///./expense_tracker.db
SECRET_KEY=your-secret-key-here
redis_url=redis://localhost:6379/0
redis_enabled=true
```

**Note:** Redis is optional. If `redis_enabled=false` or Redis is unavailable, the application will continue to work without caching and rate limiting.

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

6. Set up Redis (optional but recommended)

**Using Docker:**
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

**Using Homebrew (macOS):**
```bash
brew install redis
brew services start redis
```

**Using apt (Ubuntu/Debian):**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

The application will automatically connect to Redis on startup. If Redis is unavailable, the app will continue to work without caching and rate limiting.

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

## Caching & Rate Limiting

### Caching
- **User Summary** (`GET /users/me/summary`) - Cached for 2 minutes
- Cache is automatically invalidated when expenses or user data changes
- Redis is used for caching, but the app works without it

### Rate Limiting
- **Registration** (`POST /auth/register`) - 5 requests per 15 minutes per IP
- **Login** (`POST /auth/login`) - 10 requests per 15 minutes per IP
- Rate limit headers are included in responses: `X-RateLimit-Remaining`, `X-RateLimit-Limit`

## Project Structure

```
ExpenseTrackerAPI/
├── routes/
│   ├── __init__.py        # Package initialization
│   ├── AuthRoutes.py      # Authentication endpoints
│   ├── UserRoutes.py      # User endpoint handlers
│   └── ExpenseRoutes.py   # Expense endpoint handlers
├── auth.py                # JWT authentication utilities
├── config.py              # Database and Redis configuration
├── redis_client.py        # Redis client and caching utilities
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic validation schemas
├── main.py                # FastAPI application entry point
├── requirements.txt       # Project dependencies
└── .env                   # Environment variables (create this)
```
