from pydantic import BaseModel

# Exemple de schémas de données
class PaymentSchema(BaseModel):
    amount: float
class WithdrawSchema(BaseModel):
    amount: float