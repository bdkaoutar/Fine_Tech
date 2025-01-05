from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from Fine_Tech.backend.user_service.user.model import Wallet

class Transaction(SQLModel, table=True):
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    sender_wallet_id: int = Field(foreign_key="wallet.wallet_id")
    receiver_wallet_id: int = Field(foreign_key="wallet.wallet_id")
    amount: int = Field(gt=0)  # Montant de la transaction, doit être positif
    created_at: datetime = Field(default_factory=datetime.utcnow)

    sender_wallet: Optional["Wallet"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Transaction.sender_wallet_id]"}
    )
    receiver_wallet: Optional["Wallet"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Transaction.receiver_wallet_id]"}
    )