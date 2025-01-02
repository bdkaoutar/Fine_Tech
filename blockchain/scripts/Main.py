from web3 import Web3
from dotenv import load_dotenv
import os
import sys

#with python when running the project the files hiearchie is not recognizable
# Add the root directory to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from blockchain.logger import error_logger, transaction_logger
import json


# Load environment variables
load_dotenv()

# Environment variables
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Validate environment variables
if not INFURA_URL or not PRIVATE_KEY or not CONTRACT_ADDRESS:
    error_logger.error("Environment variables are not properly set.")
    raise ValueError("Environment variables are missing!")

# Connect to Infura
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Check connection
if web3.is_connected():
    transaction_logger.info("Connected to Ethereum network")
else:
    error_logger.error("Failed to connect to Ethereum network")
    raise ConnectionError("Failed to connect to Ethereum network")

#the contract is verified in etherscan 
# Contract ABI ==> Application Binary Interface
CONTRACT_ABI = json.loads("""[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"PaymentReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawal","type":"event"},{"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pay","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]""")

# Create contract instance
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Sender address derived from private key
SENDER_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address

# Sending Ether (to pay function)
def send_payment(amount_in_ether):
    try:
        tx = contract.functions.pay().build_transaction({
            "from": SENDER_ADDRESS,
            "value": web3.to_wei(amount_in_ether, "ether"),
            "gas": 200000,
            "gasPrice": web3.to_wei("10", "gwei"),
            "nonce": web3.eth.get_transaction_count(SENDER_ADDRESS),
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        transaction_logger.info(f"Payment transaction sent with hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        error_logger.error(f"Error in send_payment: {e}")

# Check contract balance
def check_balance():
    try:
        balance = contract.functions.getBalance().call()
        transaction_logger.info(f"Contract balance: {web3.from_wei(balance, 'ether')} ETH")
    except Exception as e:
        error_logger.error(f"Error in check_balance: {e}")

# Withdraw Ether
def withdraw_funds(amount_in_ether):
    try:
        tx = contract.functions.withdraw(web3.to_wei(amount_in_ether, "ether")).build_transaction({
            "from": SENDER_ADDRESS,
            "gas": 200000,
            "gasPrice": web3.to_wei("20", "gwei"),
            "nonce": web3.eth.get_transaction_count(SENDER_ADDRESS),
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        transaction_logger.info(f"Withdrawal transaction sent with hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        error_logger.error(f"Error in withdraw_funds: {e}")

# Example calls
#the functions are tested and verifie din etherscan 
if __name__ == "__main__":
    check_balance()
    #send_payment(0.01)  # Uncomment to send 0.01 ETH to the contract
    # withdraw_funds(0.005)  # Uncomment to withdraw 0.005 ETH