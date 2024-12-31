from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session
from Fine_Tech.backend.transaction_service.database.main import get_session
from Fine_Tech.backend.transaction_service.transaction.schema import TransactionCreate,TransactionRead
from Fine_Tech.backend.transaction_service.transaction.services import TransactionService
from Fine_Tech.backend.transaction_service.transaction.model import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    session: AsyncSession = Depends(get_session)
):
    # Perform necessary checks (e.g., validate sender and receiver wallets, balance)
    if transaction_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Transaction amount must be greater than zero.")

    sender_wallet = await TransactionService.get_wallet_by_id(session, transaction_data.sender_wallet_id)
    receiver_wallet = await TransactionService.get_wallet_by_id(session, transaction_data.receiver_wallet_id)

    if not sender_wallet or not receiver_wallet:
        raise HTTPException(status_code=404, detail="Sender or receiver wallet not found.")

    if sender_wallet.balance < transaction_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance in sender's wallet.")

    # Create a new transaction
    return await TransactionService.create_transaction(
        session,
        transaction_data.sender_wallet_id,
        transaction_data.receiver_wallet_id,
        transaction_data.amount,
        transaction_data.description
    )


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(transaction_id: int, session: AsyncSession = Depends(get_session)):
    transaction = await TransactionService.get_transaction_by_id(session, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return transaction


@router.get("/", response_model=List[TransactionRead])
async def get_transactions(session: AsyncSession = Depends(get_session)):
    return await TransactionService.get_all_transactions(session)


@router.put("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int,
    updates: dict,
    session: AsyncSession = Depends(get_session)
):
    transaction = await TransactionService.update_transaction(session, transaction_id, updates)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, session: AsyncSession = Depends(get_session)):
    success = await TransactionService.delete_transaction(session, transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return {"message": "Transaction deleted successfully."}
