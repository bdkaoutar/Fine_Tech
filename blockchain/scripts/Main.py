from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json

# because when running the project doesn't know the hiearchy of folders
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from blockchain.logger import error_logger, transaction_logger


#for privacy and security
load_dotenv()

# Retrieve environment variables for Infura URL, private key, and contract address.
#in the etherum network we are using sepolia as a test network and mining it using google cloud web3 and also sepolia pow faucet
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Validate that all required environment variables are set
if not INFURA_URL or not PRIVATE_KEY or not CONTRACT_ADDRESS:
    error_logger.error("Environment variables are not properly set.")
    raise ValueError("Environment variables are missing!")

#Initialize a connection to the Ethereum blockchain via Infura
#Infura acts as the provider through which you interact with the Ethereum network
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Verify the connection to the Ethereum network
if web3.is_connected():
    transaction_logger.info("Connected to Ethereum network")
else:
    error_logger.error("Failed to connect to Ethereum network")
    raise ConnectionError("Failed to connect to Ethereum network")

# Contract ABI (Application Binary Interface) defines the structure of the contract's methods and events.
# we used remix ide to create and deploy the contract using solidity language(it's a little bit like java use POO but have different types of variables)
# This ABI is verified and obtained from Etherscan for the deployed contract.
#we can get the abi from remix or etherscan after verifying it 
#had to json pars because they were a slite difference in false and False(Python Format)
CONTRACT_ABI = json.loads("""[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"PaymentReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawal","type":"event"},{"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pay","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]""")

# Create a contract instance using its address and ABI.
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
# to see contract details go to contracts/FintechContract.sol

# Derive the sender's address from the provided private key.
SENDER_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address

# Function to fetch current gas price dynamically
def get_current_gas_price():
    return web3.eth.gas_price

# Sending Ether (to pay function)
def send_payment(amount_in_ether):
    try:
        current_gas_price = get_current_gas_price()
        tx = contract.functions.pay().build_transaction({
            "from": SENDER_ADDRESS,
            "value": web3.to_wei(amount_in_ether, "ether"),
            "gas": 200000,# Gas limit its a limit on the resources a transaction can use
            "gasPrice": current_gas_price + web3.to_wei(2, "gwei"),  # Increase gas price slightly
             # Gas price because it is not an exactly amount everytime it changes it can be high or low we can see it in etherscan if we want to know how much
            "nonce": web3.eth.get_transaction_count(SENDER_ADDRESS),# Transaction nonce if teh transaction failed we can see it in status=0 if status=1 it is succesful 
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
        current_gas_price = get_current_gas_price()
        tx = contract.functions.withdraw(web3.to_wei(amount_in_ether, "ether")).build_transaction({
            "from": SENDER_ADDRESS,
            "gas": 200000,
            "gasPrice": current_gas_price + web3.to_wei(5, "gwei"),  
            "nonce": web3.eth.get_transaction_count(SENDER_ADDRESS),
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        transaction_logger.info(f"Withdrawal transaction sent with hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        error_logger.error(f"Error in withdraw_funds: {e}")

# Example calls
if __name__ == "__main__":
    check_balance()
    #send_payment(0.01)  # Send 0.01 ETH to the contract
    # withdraw_funds(0.005)  # Uncomment to withdraw 0.005 ETH
