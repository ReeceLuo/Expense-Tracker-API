from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Request body schema for creating user
class UserCreate(BaseModel):
    name: str
    email: str

# Request body schema for updating user
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]

# Response body schema for routes (what the API returns)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

# Request body schema for creating expense
class ExpenseCreate(BaseModel):
    user_id: int
    amount: float
    description: Optional[str]
    category: Optional[str]

# Response body schema for routes (what the API returns)
class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    description: Optional[str]
    category: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

