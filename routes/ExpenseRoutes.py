from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config import get_db
from models import Expense, User
from schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

# Create expense
@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == expense.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id: {expense.user_id} could not be found."
        )

    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# Get all expenses from user (before auth)
@router.get("/user/{user_id}", response_model=List[ExpenseResponse], status_code=status.HTTP_200_OK)
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


# Get expense (before auth)
@router.get("/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The expense with id: {expense_id} could not be found."
        )
    
    return expense


# Update expense (before auth)
@router.put("/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session=Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The expense with id: {expense_id} could not be found."
        )
    
    update_data = expense_update.model_dump(exclude_unset = True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


# Toggle expense status (before auth)
@router.patch("/{expense_id}/toggle-paid", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def toggle_paid(expense_id: int, db: Session=Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The expense with id: {expense_id} could not be found."
        )
    
    expense.paid = not expense.paid
    db.commit()
    db.refresh(expense)
    return expense

# Delete expense (before auth)
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The expense with id: {expense_id} could not be found."
        )

    db.delete(expense)
    db.commit()
    return None