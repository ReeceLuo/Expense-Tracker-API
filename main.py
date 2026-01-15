from fastapi import FastAPI
from config import engine, DeclarativeBase
from routes import ExpenseRoutes, UserRoutes, AuthRoutes

DeclarativeBase.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="An API for users to track their expenses",
    version="1.0.0"
)

app.include_router(ExpenseRoutes.router)
app.include_router(UserRoutes.router)
app.include_router(AuthRoutes.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}