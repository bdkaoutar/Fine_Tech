from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4

class Wallet(SQLModel, table=True):
    wallet_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(foreign_key="user.username", nullable=False)  # Foreign key to username
    currency: str = Field(nullable=False)  # e.g., "USD", "BTC", "ETH"
    balance: int = Field(default=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional["User"] = Relationship(back_populates="wallets")


class User(SQLModel, table=True):
    username: str = Field(default_factory=lambda: f"user_{uuid4().hex[:8]}", primary_key=True)
    full_name: str
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str
    role: str = Field(default="user")  # Added role with default value "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    disabled: bool = Field(default=False)

    wallets: List[Wallet] = Relationship(back_populates="owner")
