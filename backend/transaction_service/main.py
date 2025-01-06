from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from transaction.routes import router as routes
# Création de l'application FastAPI
app = FastAPI()
app.include_router(routes)
# Modèle pour les portefeuilles
class Wallet(BaseModel):
    id: int
    balance: float

# Modèle pour les utilisateurs
class User(BaseModel):
    id: int
    name: str
    email: str
    wallets: List[Wallet]

# Utilisateurs fictifs pour tester
fake_users = [
    User(id=1, name="Alice", email="alice@example.com", wallets=[Wallet(id=1, balance=100.0), Wallet(id=2, balance=50.0)]),
    User(id=2, name="Bob", email="bob@example.com", wallets=[Wallet(id=3, balance=200.0)]),
]

# Modèle pour la requête de transaction
class TransactionRequest(BaseModel):
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: float

class Transaction(BaseModel):
    transaction_id: str
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: float
    sender_balance_before: float
    receiver_balance_before: float
    sender_balance_after: float
    receiver_balance_after: float

# Liste des transactions effectuées
transactions = []

# Route pour afficher un message de bienvenue
@app.get("/message")
async def get_message():
    return {"message": "Bienvenue sur notre microservice de gestion des utilisateurs et des portefeuilles!"}

# Route pour récupérer les utilisateurs et leurs portefeuilles
@app.get("/users", response_model=List[User])
async def get_users():
    return fake_users

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = next((user for user in fake_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Route pour récupérer un portefeuille par ID
@app.get("/wallets/{wallet_id}", response_model=Wallet)
async def get_wallet(wallet_id: int):
    for user in fake_users:
        wallet = next((wallet for wallet in user.wallets if wallet.id == wallet_id), None)
        if wallet:
            return wallet
    raise HTTPException(status_code=404, detail="Wallet not found")

# Endpoint pour créer une transaction
@app.post("/transactions/")
async def create_transaction(transaction: TransactionRequest):
    """Effectuer une transaction entre deux portefeuilles"""
    sender_wallet = None
    receiver_wallet = None
    transaction_id = str(uuid.uuid4())  # Générer un identifiant unique pour la transaction

    # Chercher les portefeuilles
    for user in fake_users:
        for wallet in user.wallets:
            if wallet.id == transaction.sender_wallet_id:
                sender_wallet = wallet
            if wallet.id == transaction.receiver_wallet_id:
                receiver_wallet = wallet

    # Si les deux portefeuilles sont trouvés
    if not sender_wallet or not receiver_wallet:
        raise HTTPException(status_code=404, detail="One or both wallets not found")

    # Vérifier le solde du portefeuille de l'expéditeur
    if sender_wallet.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Enregistrer les soldes avant la transaction
    sender_balance_before = sender_wallet.balance
    receiver_balance_before = receiver_wallet.balance

    # Effectuer la transaction
    sender_wallet.balance -= transaction.amount
    receiver_wallet.balance += transaction.amount

    # Enregistrer la transaction
    transactions.append(Transaction(
        transaction_id=transaction_id,
        sender_wallet_id=transaction.sender_wallet_id,
        receiver_wallet_id=transaction.receiver_wallet_id,
        amount=transaction.amount,
        sender_balance_before=sender_balance_before,
        receiver_balance_before=receiver_balance_before,
        sender_balance_after=sender_wallet.balance,
        receiver_balance_after=receiver_wallet.balance
    ))

    return {
        "transaction_id": transaction_id,
        "message": "Transaction successful",
        "sender_wallet_balance": sender_wallet.balance,
        "receiver_wallet_balance": receiver_wallet.balance
    }

# Route pour annuler une transaction
@app.delete("/transactions/{transaction_id}/cancel")
async def cancel_transaction(transaction_id: str):
    transaction_to_cancel = next((txn for txn in transactions if txn.transaction_id == transaction_id), None)

    if not transaction_to_cancel:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Trouver les portefeuilles liés à la transaction
    sender_wallet = next((wallet for user in fake_users for wallet in user.wallets if wallet.id == transaction_to_cancel.sender_wallet_id), None)
    receiver_wallet = next((wallet for user in fake_users for wallet in user.wallets if wallet.id == transaction_to_cancel.receiver_wallet_id), None)

    if not sender_wallet or not receiver_wallet:
        raise HTTPException(status_code=404, detail="Wallets not found")

    # Annuler la transaction
    sender_wallet.balance = transaction_to_cancel.sender_balance_before
    receiver_wallet.balance = transaction_to_cancel.receiver_balance_before

    # Supprimer la transaction
    transactions.remove(transaction_to_cancel)

    return {
        "message": "Transaction cancelled successfully",
        "sender_wallet_balance": sender_wallet.balance,
        "receiver_wallet_balance": receiver_wallet.balance
    }

# Test pour s'assurer que le microservice fonctionne
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
