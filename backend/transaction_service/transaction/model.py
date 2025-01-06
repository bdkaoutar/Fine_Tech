from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
import httpx  # Utilisé pour appeler l'API du microservice User


class Transaction(SQLModel, table=True):
    """Modèle représentant une transaction entre deux portefeuilles."""
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    sender_wallet_id: int = Field(foreign_key="wallet.wallet_id")
    receiver_wallet_id: int = Field(foreign_key="wallet.wallet_id")
    amount: float = Field(gt=0)  # Le montant de la transaction, doit être positif
    created_at: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None

    async def process_transaction(self, user_service_url: str) -> bool:
        """Traitement de la transaction avec validation des soldes via l'API du microservice User."""

        # Vérification des soldes des portefeuilles via API
        async with httpx.AsyncClient() as client:
            sender_wallet_response = await client.get(f"{user_service_url}/wallets/{self.sender_wallet_id}")
            receiver_wallet_response = await client.get(f"{user_service_url}/wallets/{self.receiver_wallet_id}")

            if sender_wallet_response.status_code != 200:
                raise ValueError("Portefeuille de l'expéditeur introuvable ou erreur dans le microservice utilisateur.")
            if receiver_wallet_response.status_code != 200:
                raise ValueError("Portefeuille du récepteur introuvable ou erreur dans le microservice utilisateur.")

            sender_wallet = sender_wallet_response.json()
            receiver_wallet = receiver_wallet_response.json()

            # Vérification du solde du portefeuille de l'expéditeur
            if sender_wallet['balance'] < self.amount:
                raise ValueError("Solde insuffisant dans le portefeuille de l'expéditeur.")

            # Si tout est bon, mettre à jour les soldes des portefeuilles via des appels API POST ou PUT
            # Mise à jour du portefeuille de l'expéditeur
            await client.put(f"{user_service_url}/wallets/{self.sender_wallet_id}",
                             json={"balance": sender_wallet['balance'] - self.amount})
            # Mise à jour du portefeuille du récepteur
            await client.put(f"{user_service_url}/wallets/{self.receiver_wallet_id}",
                             json={"balance": receiver_wallet['balance'] + self.amount})

        return True
