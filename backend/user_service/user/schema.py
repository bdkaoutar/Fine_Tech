from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str

class UserRead(BaseModel):
    user_id: Optional[int]
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
