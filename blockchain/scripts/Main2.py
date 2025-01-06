from web3 import Web3
from dotenv import load_dotenv
import os
import sys

# because when running the project doesn't know the hiearchy of folders
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from blockchain.logger import error_logger, transaction_logger
import json

#for privacy and security
load_dotenv()

# Retrieve environment variables for Infura URL, private key, and contract address.
#in the etherum network we are using sepolia as a test network and mining it using google cloud web3 and also sepolia pow faucet
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Validate that all required environment variables are set.
if not INFURA_URL or not PRIVATE_KEY or not CONTRACT_ADDRESS:
    error_logger.error("Environment variables are not properly set.")
    raise ValueError("Environment variables are missing!")

#Initialize a connection to the Ethereum blockchain via Infura
#Infura acts as the provider through which you interact with the Ethereum network
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Verify the connection to the Ethereum network.
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
CONTRACT_ABI = json.loads("""[
    {"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
    {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"PaymentReceived","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawal","type":"event"},
    {"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"pay","outputs":[],"stateMutability":"payable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}
]""")

# Create a contract instance using its address and ABI.
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
# to see contract details go to contracts/FintechContract.sol

# Derive the sender's address from the provided private key.
SENDER_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address

def send_payment(amount_in_ether):
    try:
        # Get the current nonce
        nonce = web3.eth.get_transaction_count(SENDER_ADDRESS)
        print(f"Current nonce: {nonce}")
        
        # Check for pending transactions
        pending_tx = web3.eth.get_block('pending')
        if pending_tx:
            print(f"Pending transactions: {pending_tx}")
            # Wait for pending transactions to be mined (optional)
            print("Waiting for previous transactions to be mined...")
        
        # Build the transaction details.
        tx = contract.functions.pay().build_transaction({
            "from": SENDER_ADDRESS, 
            "value": web3.to_wei(amount_in_ether, "ether"),  # Amount in wei
            "gas": 200000,  # Gas limit
            "gasPrice": web3.to_wei("10", "gwei"),  # Gas price
            "nonce": nonce,  # Use the correct nonce
        })

        # Sign the transaction with the private key.
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)

        # Send the signed transaction to the Ethereum network.
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Log the transaction hash for tracking
        transaction_logger.info(f"Payment transaction sent with hash: {web3.to_hex(tx_hash)}")
        
        # Wait for the transaction to be mined
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Transaction receipt: {receipt}")

    except Exception as e:
        # Log any errors encountered during the payment process
        error_logger.error(f"Error in send_payment: {e}")


# Function to send payment to the contract's `pay` function.
# def send_payment(amount_in_ether):
#     try:
#         nonce = web3.eth.get_transaction_count(SENDER_ADDRESS)
#         print(f"Current nonce: {nonce}")
#         # Build the transaction details.
#         tx = contract.functions.pay().build_transaction({
#             "from": SENDER_ADDRESS, 
#             "value": web3.to_wei(amount_in_ether, "ether"),  # Amount in wei
#             "gas": 200000,  # Gas limit its a limit on the resources a transaction can use
#             "gasPrice": web3.to_wei("10", "gwei"),  # Gas price because it is not an exactly amount everytime it changes it can be high or low we can see it in etherscan if we want to know how much
#             "nonce": nonce  # Transaction nonce if teh transaction failed we can see it in status=0 if status=1 it is succesful 
#         })

#         # Sign the transaction with the private key.
#         signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)

#         # Send the signed transaction to the Ethereum network.
#         tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

#         # Log the transaction hash for tracking.
#         transaction_logger.info(f"Payment transaction sent with hash: {web3.to_hex(tx_hash)}")

#         # Wait for the transaction receipt (confirmation)
#         tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
#         print(f"Transaction receipt: {tx_receipt}")

#         # Once confirmed, check the balance again
#         if tx_receipt['status'] == 1:  # Check if the transaction was successful
#             balance = contract.functions.getBalance().call()
#             transaction_logger.info(f"Contract balance updated: {web3.from_wei(balance, 'ether')} ETH")
#         else:
#             error_logger.error("Transaction failed.")
#     except Exception as e:
#         # Log any errors encountered during the payment process
#         error_logger.error(f"Error in send_payment: {e}")
#/////////////////////////////////////////////////////////////////////

    #     # Sign the transaction with the private key.
    #     signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    #     # Send the signed transaction to the Ethereum network.
    #     tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    #     # Log the transaction hash for tracking very -->important to have a history of transactions 
    #     #exemple '2024-12-31 12:54:47,718 - INFO - Payment transaction sent with hash: 0x2a25ada928343d7113d0a5c45ddbe9ab5ca6f1fefa9b65dfdcf6bc6b83d9c1f4'
    #     transaction_logger.info(f"Payment transaction sent with hash: {web3.to_hex(tx_hash)}")
    # except Exception as e:
    #     # Log any errors encountered during the payment process 
    #     error_logger.error(f"Error in send_payment: {e}")

# Function to check the balance of the contract.
def check_balance():
    try:
        # Call the `getBalance` function from the smart contract.
        balance = contract.functions.getBalance().call()

        # Log the contract balance in Ether.
        transaction_logger.info(f"Contract balance: {web3.from_wei(balance, 'ether')} ETH")
    except Exception as e:
        # Log any errors encountered during balance retrieval.
        error_logger.error(f"Error in check_balance: {e}")

# Function to withdraw funds from the contract using the `withdraw` function.
def withdraw_funds(amount_in_ether):
    try:
        # Build the transaction details for the withdrawal.
        tx = contract.functions.withdraw(web3.to_wei(amount_in_ether, "ether")).build_transaction({
            "from": SENDER_ADDRESS,  # Sender address
            "gas": 200000,  # Gas limit
            "gasPrice": web3.to_wei("20", "gwei"),  # Gas price
            "nonce": web3.eth.get_transaction_count(SENDER_ADDRESS),  # Transaction nonce
        })

        # Sign the transaction with the private key.
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)

        # Send the signed transaction to the Ethereum network.
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Log the transaction hash for tracking.
        transaction_logger.info(f"Withdrawal transaction sent with hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        # Log any errors encountered during the withdrawal process.
        error_logger.error(f"Error in withdraw_funds: {e}")

# Example calls to demonstrate functionality.
# These calls are commented out to prevent accidental execution.
if __name__ == "__main__":
    # Check the contract's current balance.
    check_balance()

    # Uncomment the lines below to test payment and withdrawal functions.
    send_payment(0.001)  # Sends 0.01 ETH to the contract.
    check_balance()
    # withdraw_funds(0.005)  # Withdraws 0.005 ETH from the contract.
