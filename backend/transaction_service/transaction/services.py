from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from Fine_Tech.backend.transaction_service.transaction.repository import TransactionRepository
from Fine_Tech.backend.transaction_service.transaction.model import Transaction


class TransactionService:
    @staticmethod
    async def create_transaction(
        session: AsyncSession,
        sender_wallet_id: int,
        receiver_wallet_id: int,
        amount: float,
        description: Optional[str] = None
    ) -> Transaction:
        """Créer une nouvelle transaction."""
        transaction = Transaction(
            sender_wallet_id=sender_wallet_id,
            receiver_wallet_id=receiver_wallet_id,
            amount=amount,
            description=description
        )
        return await TransactionRepository.create_transaction(session, transaction)

    @staticmethod
    async def get_transaction_by_id(session: AsyncSession, transaction_id: int) -> Optional[Transaction]:
        """Récupérer une transaction par son ID."""
        return await TransactionRepository.get_transaction_by_id(session, transaction_id)

    @staticmethod
    async def get_all_transactions(session: AsyncSession) -> List[Transaction]:
        """Récupérer toutes les transactions."""
        return await TransactionRepository.get_all_transactions(session)

    @staticmethod
    async def update_transaction(session: AsyncSession, transaction_id: int, updates: dict) -> Optional[Transaction]:
        """Mettre à jour une transaction."""
        return await TransactionRepository.update_transaction(session, transaction_id, updates)

    @staticmethod
    async def delete_transaction(session: AsyncSession, transaction_id: int) -> bool:
        """Supprimer une transaction."""
        return await TransactionRepository.delete_transaction(session, transaction_id)
