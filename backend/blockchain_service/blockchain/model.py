from datetime import datetime
from sqlmodel import Field, SQLModel

class BlockchainTransaction(SQLModel, table=True):
    transaction_id: int = Field(default=None, primary_key=True)
    sender_address: str = Field(index=True)  # Adresse blockchain de l'expéditeur
    receiver_address: str = Field(index=True)  # Adresse blockchain du destinataire
    amount: float = Field(gt=0)  # Montant de la transaction
    status: str = Field(default="PENDING")  # Statut : PENDING, CONFIRMED, FAILED
    tx_hash: str = Field(default=None)  # Hash de la transaction sur la blockchain
    created_at: datetime = Field(default_factory=datetime.utcnow)
