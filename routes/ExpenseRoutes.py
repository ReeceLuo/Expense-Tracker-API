from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config import get_db
from models import Expense, User
from schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from auth import get_current_user


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

# Create expense
@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_expense = Expense(
        user_id=current_user.id,
        amount=expense.amount,
        paid=expense.paid,
        description=expense.description,
        category=expense.category
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# Get all expenses from user
@router.get("/user", response_model=List[ExpenseResponse], status_code=status.HTTP_200_OK)
def get_user_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return user_expenses


# Get expense
@router.get("/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def get_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The expense with id: {expense_id} could not be found."
        )
    
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to view this expense."
        )
    
    return expense


# Update expense
@router.put("/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def update_expense(
    expense_id: int, 
    expense_update: ExpenseUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The expense with id: {expense_id} could not be found."
        )
    
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to edit this expense"
        )
    
    update_data = expense_update.model_dump(exclude_unset = True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


# Toggle expense status
@router.patch("/{expense_id}/toggle-paid", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def toggle_paid(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The expense with id: {expense_id} could not be found."
        )
    
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to edit this expense."
        )
    
    expense.paid = not expense.paid
    db.commit()
    db.refresh(expense)
    return expense

# Delete expense
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The expense with id: {expense_id} could not be found."
        )
    
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to delete this expense"
        )

    db.delete(expense)
    db.commit()
    return None