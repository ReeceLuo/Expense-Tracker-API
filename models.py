from sqlalchemy import Column, Integer, Double, String, Boolean, DateTime
from sqlalchemy.orm import func
from config import DeclarativeBase


# User database model
class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    # hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_defualt=func.now(), nullable=False)


# Expense database model
class Expense(DeclarativeBase):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Double, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
