from datetime import datetime
from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from transaction.model import Transaction


class TransactionRepository:
    @staticmethod
    async def create_transaction(session: AsyncSession, transaction: Transaction) -> Transaction:
        """Create a new transaction."""
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction

    @staticmethod
    async def get_transaction_by_id(session: AsyncSession, transaction_id: int) -> Optional[Transaction]:
        """Fetch a transaction by its ID."""
        return await session.get(Transaction, transaction_id)

    @staticmethod
    async def get_all_transactions(session: AsyncSession) -> List[Transaction]:
        """Fetch all transactions."""
        result = await session.execute(select(Transaction))
        return result.scalars().all()

    @staticmethod
    async def update_transaction(session: AsyncSession, transaction_id: int, updates: dict) -> Transaction:
        """Mettre à jour une transaction et gérer les erreurs."""
        # Récupérer la transaction à mettre à jour
        transaction = await session.get(Transaction, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found.")

        # Appliquer les mises à jour
        for key, value in updates.items():
            setattr(transaction, key, value)

        # Commit des changements dans la base de données
        await session.commit()
        await session.refresh(transaction)

        return transaction

    @staticmethod
    async def delete_transaction(session: AsyncSession, transaction_id: int) -> bool:
        """Delete a transaction by its ID."""
        transaction = await session.get(Transaction, transaction_id)
        if transaction:
            await session.delete(transaction)
            await session.commit()
            return True
        return False
