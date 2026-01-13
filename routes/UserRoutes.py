from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from config import get_db
from models import User, Expense
from schemas import UserCreate, UserUpdate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Create user
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session=Depends(get_db)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get user summary
@router.get("/{user_id}/summary", status_code=status.HTTP_200_OK)
def get_total_user_expenses(user_id: int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id: {user_id} could not be found."
        )
    
    total_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).scalar() or 0.0
    total_paid = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        Expense.paid == True
    ).scalar() or 0.0
    remaining_budget = user.budget - total_paid

    num_expenses_paid = db.query(Expense).filter(
        Expense.user_id == user_id, 
        Expense.paid == True # (could just be expense.paid)
    ).count()
    num_expenses = db.query(Expense).filter(Expense.user_id == user_id).count()

    return {"User": user.name, 
            "Total expenses to pay": total_expenses,
            "Expenses paid": f"{num_expenses_paid} / {num_expenses}",
            "Budget": user.budget,
            "Total paid": total_paid,
            "Remaining budget": remaining_budget,
            "Status": "Over budget" if remaining_budget < 0 else "On track"}


# Get user
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id: {user_id} could not be found."
        )
    
    return user


# Update user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id: {user_id} could not be found."
        )
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


# Temporary delete route
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id: {user_id} could not be found."
        )
    
    db.delete(user)
    db.commit()
    return None