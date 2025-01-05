from datetime import datetime
from pydantic import BaseModel

class BlockchainTransactionCreate(BaseModel):
    sender_address: str
    receiver_address: str
    amount: float

class BlockchainTransactionRead(BaseModel):
    transaction_id: int
    sender_address: str
    receiver_address: str
    amount: float
    status: str
    tx_hash: str
    created_at: datetime

class BlockchainTransactionUpdate(BaseModel):
    status: str
    tx_hash: str
