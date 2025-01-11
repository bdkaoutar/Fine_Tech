from pydantic import BaseModel

# Exemple de modèle pour les requêtes et réponses
class PaymentRequest(BaseModel):
    amount: float

class BalanceResponse(BaseModel):
    balance: float

class WithdrawRequest(BaseModel):
    amount: float