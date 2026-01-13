from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from config import DeclarativeBase


# User database model
class User(DeclarativeBase):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    # hashed_password: Mapped[str] = mapped_column(nullable=False)
    budget: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    expenses: Mapped[List["Expense"]] = relationship(back_populates="user")
    # "Expense" is a forward reference to the Expense model class
    # "user" is the attribute name in the Expense class


# Expense database model
class Expense(DeclarativeBase):
    __tablename__ = "expense_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(back_populates="expenses")
    # "expenses" is the attribute name in the User class 

    # "expense.user = new_user" would update the user_id attribute
    # relationship() establishes the relationship, the ORM finds attribute in Expense w/ ForeignKey

    amount: Mapped[float] = mapped_column(nullable=False)
    paid: Mapped[bool] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    category: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )