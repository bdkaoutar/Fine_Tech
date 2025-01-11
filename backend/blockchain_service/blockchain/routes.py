from fastapi import APIRouter, HTTPException
from blockchain.services import BlockchainService
from pydantic import BaseModel


class PaymentSchema(BaseModel):
    amount: float
class WithdrawRequest(BaseModel):
    amount: float
blockchain_routes = APIRouter()

# La route qui affiche un message
@blockchain_routes.get("/hello")
async def display_message():
    return {"message": "Bienvenue dans mon service Blockchain "}

# la route post qui envoie un paiement
@blockchain_routes.post("/send_payment")
async def send_payment(payment: PaymentSchema):
    try:
        blockchain_service = BlockchainService()
        blockchain_service.send_payment(payment.amount)
        return {"message": "Payment sent successfully!"}
    except Exception as e:
        return {"error": str(e)}

# la route get pour vérifie le solde
@blockchain_routes.get("/balance")
async def get_balance():
    try:
        blockchain_service = BlockchainService()
        balance = blockchain_service.check_balance()
        return {"balance": balance}
    except Exception as e:
        return {"error": str(e)}

#la route post qui retirer des fonds
# Cette route permet à un utilisateur de retirer des fonds du contrat blockchain.
@blockchain_routes.post("/withdraw-funds")
async def withdraw_funds(payment: PaymentSchema):
    try:
        blockchain_service = BlockchainService()
        tx_hash = blockchain_service.withdraw_funds(payment.amount)
        return {"message": "Withdrawal transaction sent successfully", "tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))