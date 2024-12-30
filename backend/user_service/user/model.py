from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class Wallet(SQLModel, table=True):
    wallet_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    balance: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional["User"] = Relationship(back_populates="wallets")


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    wallets: List[Wallet] = Relationship(back_populates="owner")


