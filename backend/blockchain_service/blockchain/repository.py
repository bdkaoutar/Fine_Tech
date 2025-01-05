from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Fine_Tech.backend.blockchain_service.blockchain.model import BlockchainTransaction

class BlockchainTransactionRepository:
    @staticmethod
    async def create_transaction(session: AsyncSession, transaction_data: BlockchainTransaction):
        session.add(transaction_data)
        await session.commit()
        await session.refresh(transaction_data)
        return transaction_data

    @staticmethod
    async def get_transaction_by_id(session: AsyncSession, transaction_id: int):
        query = select(BlockchainTransaction).where(BlockchainTransaction.transaction_id == transaction_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_transaction(session: AsyncSession, transaction_id: int, updates: dict):
        transaction = await BlockchainTransactionRepository.get_transaction_by_id(session, transaction_id)
        if not transaction:
            return None
        for key, value in updates.items():
            setattr(transaction, key, value)
        await session.commit()
        return transaction
