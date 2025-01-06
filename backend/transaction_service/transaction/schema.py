from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class TransactionCreate(BaseModel):
    sender_wallet_id: int
    receiver_wallet_id: int
    sender_user_id: int
    receiver_user_id: int
    amount: float
    description: Optional[str] = None

class TransactionRead(BaseModel):
    transaction_id: int
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: float
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
