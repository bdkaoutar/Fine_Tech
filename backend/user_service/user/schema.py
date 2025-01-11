from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional


# Enum for user roles
class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"


# Token schema for authentication
class Token(BaseModel):
    access_token: str
    token_type: str


# Token data schema
class TokenData(BaseModel):
    username: Optional[str] = None  # Using Optional for consistency


# Base schema for user-related operations
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: RoleEnum = RoleEnum.user  # Use the Enum directly
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Schema for creating a new user
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str  # Users provide these three fields

# Schema for user data in the database
class UserInDB(UserBase):
    hashed_password: str

# Schema for updating user profile
class UserUpdateProfile(BaseModel):
    email: Optional[EmailStr] = None  # Allow updating email
    full_name: Optional[str] = None  # Optional full name update
    password: Optional[str] = None  # Allow updating password


# Schema for updating user data (e.g., admin use)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None  # Use RoleEnum for role updates


# Schema for creating a wallet
class WalletCreate(BaseModel):
    currency: str
    balance: int = 1000


# Schema for reading wallet data
class WalletRead(BaseModel):
    wallet_id: int
    username: str
    currency: str
    balance: int
    created_at: datetime


# Schema for reading user data
class UserRead(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    role: RoleEnum
    disabled: bool  # Ensure this field is always included in the response
