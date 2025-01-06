from fastapi import APIRouter, HTTPException, Depends
from transaction.schema import TransactionCreate, TransactionRead, TransactionUpdate
from transaction.services import TransactionService
import httpx

router = APIRouter()

# URL de base de votre microservice user_service
USER_SERVICE_URL = "http://localhost:8080"

@router.get("/hello")
async def read_root():
    return {"message": "Welcome to my Transaction Service API!"}


# Créer une nouvelle transaction
@router.post("/transactions/", response_model=TransactionRead, status_code=201)
async def create_transaction(
    transaction_data: TransactionCreate
):
    # Consommer les microservices user_service pour récupérer les portefeuilles
    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"{USER_SERVICE_URL}/users/{transaction_data.sender_user_id}")
        receiver_response = await client.get(f"{USER_SERVICE_URL}/users/{transaction_data.receiver_user_id}")

        if user_response.status_code != 200 or receiver_response.status_code != 200:
            raise HTTPException(status_code=404, detail="User(s) not found")

        sender_user = user_response.json()
        receiver_user = receiver_response.json()

        sender_wallet = next((wallet for wallet in sender_user["wallets"] if wallet["id"] == transaction_data.sender_wallet_id), None)
        receiver_wallet = next((wallet for wallet in receiver_user["wallets"] if wallet["id"] == transaction_data.receiver_wallet_id), None)

        if not sender_wallet or not receiver_wallet:
            raise HTTPException(status_code=404, detail="Wallets not found")

        # Vérifier le solde du portefeuille de l'expéditeur
        if sender_wallet["balance"] < transaction_data.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Appeler le service TransactionService pour créer la transaction
        transaction = await TransactionService.create_transaction(
            sender_wallet_id=transaction_data.sender_wallet_id,
            receiver_wallet_id=transaction_data.receiver_wallet_id,
            amount=transaction_data.amount
        )

        return transaction

# Mettre à jour une transaction
@router.put("/transactions/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
        transaction_id: int,
        updates: TransactionUpdate
):
    try:
        # Appeler le service TransactionService pour mettre à jour la transaction
        transaction = await TransactionService.update_transaction(transaction_id, updates.dict(exclude_unset=True))
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the transaction: {str(e)}")

# Supprimer une transaction (Annuler une transaction)
@router.delete("/transactions/{transaction_id}", status_code=204)
async def cancel_transaction(transaction_id: int):
    try:
        # Appeler le service TransactionService pour annuler la transaction
        success = await TransactionService.cancel_transaction(transaction_id)
        if not success:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return {"message": "Transaction cancelled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while cancelling the transaction: {str(e)}")

# Optionnel : Récupérer toutes les transactions (pour les tests)
@router.get("/transactions/", response_model=list[TransactionRead])
async def get_all_transactions():
    try:
        return await TransactionService.get_all_transactions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Optionnel : Récupérer une transaction par ID (pour les tests)
@router.get("/transactions/{transaction_id}", response_model=TransactionRead)
async def get_transaction(transaction_id: int):
    try:
        transaction = await TransactionService.get_transaction_by_id(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found.")
        return transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
