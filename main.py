from fastapi import FastAPI
from config import engine, DeclarativeBase
from routes import ExpenseRoutes, UserRoutes, AuthRoutes
from redis_client import get_redis_client

app = FastAPI(
    title="Expense Tracker API",
    description="An API for users to track their expenses",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    """Initialize database tables and Redis connection on startup"""
    # Create database tables
    try:
        # Drop all tables first to ensure schema matches models
        DeclarativeBase.metadata.drop_all(bind=engine)
        print("Dropped existing tables")
        
        # Create all tables based on models
        DeclarativeBase.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise
    
    # Initialize Redis connection
    get_redis_client()

app.include_router(ExpenseRoutes.router)
app.include_router(UserRoutes.router)
app.include_router(AuthRoutes.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}