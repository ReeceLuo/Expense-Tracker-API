from fastapi import FastAPI
from config import engine, DeclarativeBase
from routes import ExpenseRoutes, UserRoutes, AuthRoutes

app = FastAPI(
    title="Expense Tracker API",
    description="An API for users to track their expenses",
    version="1.0.0"
)

@app.on_event("startup")
def create_tables():
    """Drop and recreate database tables on startup"""
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

app.include_router(ExpenseRoutes.router)
app.include_router(UserRoutes.router)
app.include_router(AuthRoutes.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}