from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from transaction.repository import TransactionRepository
from transaction.model import Transaction
from sqlalchemy.future import select
from pydantic import BaseModel
class Wallet(BaseModel):
    id: int
    balance: float
class TransactionService:
    @staticmethod
    async def get_wallet_by_id(session: AsyncSession, wallet_id: int) -> Optional[Wallet]:
        """Récupérer un portefeuille par son ID."""
        async with session.begin():
            stmt = select(Wallet).where(Wallet.id == wallet_id)
            result = await session.execute(stmt)
            wallet = result.scalar_one_or_none()  # Renvoie None si le portefeuille n'est pas trouvé
            return wallet

    @staticmethod
    async def create_transaction(
            session: AsyncSession,
            sender_wallet_id: int,
            receiver_wallet_id: int,
            amount: float,
            description: Optional[str] = None
    ) -> Transaction:
        # Vérifier si les portefeuilles existent
        sender_wallet = await session.get(Wallet, sender_wallet_id)
        receiver_wallet = await session.get(Wallet, receiver_wallet_id)

        if not sender_wallet or not receiver_wallet:
            raise HTTPException(status_code=404, detail="Sender or receiver wallet not found.")

        # Vérifier le solde de l'expéditeur
        if sender_wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance in sender's wallet.")

        # Déduire le montant de l'expéditeur et ajouter au destinataire
        sender_wallet.balance -= amount
        receiver_wallet.balance += amount

        # Créer la transaction
        transaction = Transaction(
            sender_wallet_id=sender_wallet_id,
            receiver_wallet_id=receiver_wallet_id,
            amount=amount,
            description=description
        )
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)

        return transaction

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

    @staticmethod
    async def cancel_transaction(session: AsyncSession, transaction_id: int) -> bool:
        """Annuler une transaction et rétablir les soldes des portefeuilles."""
        # Récupérer la transaction à annuler
        transaction = await session.get(Transaction, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found.")

        # Récupérer les portefeuilles de l'expéditeur et du récepteur
        sender_wallet = await session.get(Wallet, transaction.sender_wallet_id)
        receiver_wallet = await session.get(Wallet, transaction.receiver_wallet_id)

        if not sender_wallet or not receiver_wallet:
            raise HTTPException(status_code=404, detail="Wallet not found.")

        # Rétablir les soldes des portefeuilles
        sender_wallet.balance += transaction.amount
        receiver_wallet.balance -= transaction.amount

        # Supprimer la transaction
        await session.delete(transaction)
        await session.commit()

        return True