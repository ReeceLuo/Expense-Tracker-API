from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from config import get_db
from models import Expense, User
from schemas import ExpenseCreate, ExpenseResponse


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

# Create expense
@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session=Depends(get_db)):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

# Get all expenses from user
@router.get("/user/{user_id}", response_model=List[ExpenseResponse])
def get_user_expenses(user_id: int, db: Session=Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id: {user_id} could not be found."
        )

    user_expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    
    return user_expenses


@router.get("/user/{user_id}/summary")
def get_total_user_expenses(user_id: int, db: Session=Depends(get_db)):
     # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id: {user_id} could not be found."
        )
    
    total = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).scalar()
    return {"User": user.name, 
            "Total Expenses": total}