from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from Fine_Tech.backend.blockchain_service.database.main import get_session
from Fine_Tech.backend.blockchain_service.blockchain.schema import BlockchainTransactionCreate, BlockchainTransactionRead
from Fine_Tech.backend.blockchain_service.blockchain.services import BlockchainTransactionService
from Fine_Tech.backend.blockchain_service.blockchain.repository import BlockchainTransactionRepository

# Routeur pour Blockchain
blockchain_router = APIRouter(prefix="/blockchain", tags=["Blockchain Transactions"])



# Route pour créer une transaction
@blockchain_router.post("/", response_model=BlockchainTransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: BlockchainTransactionCreate, session: AsyncSession = Depends(get_session)
):
    try:
        # Appeler la logique de création de la transaction
        transaction = await BlockchainTransactionService.create_blockchain_transaction(
            session,
            transaction_data.sender_address,
            transaction_data.receiver_address,
            transaction_data.amount,
        )
        return transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")

# Route pour obtenir une transaction par son ID
@blockchain_router.get("/{transaction_id}", response_model=BlockchainTransactionRead)
async def get_transaction(transaction_id: int, session: AsyncSession = Depends(get_session)):
    # Récupérer la transaction en utilisant l'ID
    transaction = await BlockchainTransactionRepository.get_transaction_by_id(session, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return transaction
