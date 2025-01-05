from web3 import Web3
from sqlalchemy.ext.asyncio import AsyncSession
from  Fine_Tech.backend.blockchain_service.blockchain.model import BlockchainTransaction
from Fine_Tech.backend.blockchain_service.blockchain.repository import BlockchainTransactionRepository

# Configuration de la blockchain
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

class BlockchainTransactionService:
    @staticmethod
    async def create_blockchain_transaction(
        session: AsyncSession, sender_address: str, receiver_address: str, amount: float
    ):
        # Construire et envoyer la transaction blockchain
        nonce = web3.eth.get_transaction_count(sender_address)
        transaction = {
            "to": receiver_address,
            "value": web3.toWei(amount, "ether"),
            "gas": 21000,
            "gasPrice": web3.toWei("20", "gwei"),
            "nonce": nonce,
        }
        # ⚠️ Clé privée nécessaire pour signer la transaction
        private_key = "YOUR_PRIVATE_KEY"
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Enregistrer dans la base de données
        db_transaction = BlockchainTransaction(
            sender_address=sender_address,
            receiver_address=receiver_address,
            amount=amount,
            tx_hash=web3.toHex(tx_hash),
        )
        return await BlockchainTransactionRepository.create_transaction(session, db_transaction)

    @staticmethod
    async def get_transaction_status(tx_hash: str):
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        return receipt["status"] if receipt else "PENDING"
