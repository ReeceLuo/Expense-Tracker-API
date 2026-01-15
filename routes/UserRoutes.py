from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from config import get_db
from models import User, Expense
from schemas import UserUpdate, UserResponse
from auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Get user summary
@router.get("/me/summary", status_code=status.HTTP_200_OK)
def get_total_user_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).scalar() or 0.0
    total_paid = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.paid == True
    ).scalar() or 0.0
    remaining_budget = current_user.budget - total_paid

    num_expenses_paid = db.query(Expense).filter(
        Expense.user_id == current_user.id, 
        Expense.paid == True # (could just be expense.paid)
    ).count()
    num_expenses = db.query(Expense).filter(Expense.user_id == current_user.id).count()

    return {"User": current_user.name, 
            "Total expenses to pay": total_expenses,
            "Expenses paid": f"{num_expenses_paid} / {num_expenses}",
            "Budget": current_user.budget,
            "Total paid": total_paid,
            "Remaining budget": remaining_budget,
            "Status": "Over budget" if remaining_budget < 0 else "On track"}


# Get user
@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(current_user: User = Depends(get_current_user)):
    return current_user


# Update user
@router.put("/me", response_model=UserResponse)
def update_user(
    user_update: UserUpdate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


# Temporary delete route
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return None