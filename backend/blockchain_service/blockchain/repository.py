import json
import os
from dotenv import load_dotenv
from web3 import Web3
from logger import error_logger, transaction_logger

# for privacy and security
load_dotenv()

# Retrieve environment variables for Infura URL, private key, and contract address.
#in the etherum network we are using sepolia as a test network and mining it using google cloud web3 and also sepolia pow faucet
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

#Initialize a connection to the Ethereum blockchain via Infura
#Infura acts as the provider through which you interact with the Ethereum network
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Charger l'ABI depuis (contracts/abi.json) et initialiser le contrat
# Contract ABI (Application Binary Interface) defines the structure of the contract's methods and events.
# we used remix ide to create and deploy the contract using solidity language(it's a little bit like java use POO but have different types of variables)
# This ABI is verified and obtained from Etherscan for the deployed contract.
#we can get the abi from remix or etherscan after verifying it
#had to json pars because they were a slite difference in false and False(Python Format)
try:
    with open("contracts/abi.json") as f:
        CONTRACT_ABI = json.load(f)
    # Create a contract instance using its address and ABI.
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    # to see contract details go to contracts/FintechContract.sol
    # Derive the sender's address from the provided private key.
    SENDER_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address
    transaction_logger.info("Connected to Ethereum and contract initialized successfully.")
except Exception as e:
    error_logger.error(f"Error during initialization: {e}")
    raise

# Classe BlockchainRepository : fournir des méthodes pour interagir avec la blockchain
class BlockchainRepository:
    def __init__(self):
        #Initialisation du dépôt blockchain. Se connecte au contrat et définit l'adresse de l'expéditeur.
        try:
            self.contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
            self.sender_address = SENDER_ADDRESS
            self.web3 = web3
            transaction_logger.info("BlockchainRepository initialized successfully.")
        except Exception as e:
            error_logger.error(f"Error during BlockchainRepository initialization: {e}")
            raise

    # Sending Ether (to pay function from contract solidity)
    def send_transaction(self, amount_in_ether):
        #Envoie une transaction au contrat.
        try:
            current_gas_price = self.web3.eth.gas_price
            tx = self.contract.functions.pay().build_transaction({
                "from": self.sender_address,
                "value": self.web3.to_wei(amount_in_ether, "ether"),
                "gas": 200000,# Gas limit its a limit on the resources a transaction can use
                "gasPrice": current_gas_price + self.web3.to_wei(2, "gwei"),# Increase gas price slightly
                # Gas price because it is not an exactly amount everytime it changes it can be high or low we can see it in etherscan if we want to know how much
                "nonce": self.web3.eth.get_transaction_count(self.sender_address),# Transaction nonce if teh transaction failed we can see it in status=0 if status=1 it is succesful
            })
            # Signer la transaction avec la clé privée
            signed_tx = self.web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            # Envoyer la transaction signée
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            transaction_logger.info(f"Transaction sent successfully. Hash: {self.web3.to_hex(tx_hash)}")
            return tx_hash
        except Exception as e:
            error_logger.error(f"Error in send_transaction: {e}")
            raise

    # Récupérer le solde du contrat
    def get_balance(self):
        try:
            # Appeler la fonction getBalance() du contrat pour obtenir le solde
            balance = self.contract.functions.getBalance().call()
            # Convertir le solde de Wei à Ether
            eth_balance = self.web3.from_wei(balance, 'ether')
            transaction_logger.info(f"Balance retrieved successfully: {eth_balance} ETH")
            return eth_balance
        except Exception as e:
            error_logger.error(f"Error in get_balance: {e}")
            raise

    # Function to fetch current gas price dynamically
    def get_current_gas_price(self):
        try:
            return self.web3.eth.gas_price
        except Exception as e:
            error_logger.error(f"Error in get_current_gas_price: {e}")
            raise

    # Effectuer un retrait de fonds
    def withdraw_funds(self, amount_in_ether):
        try:
            # Récupérer le prix actuel du gaz
            current_gas_price = self.get_current_gas_price()
            # Créer une transaction pour appeler la fonction withdraw() du contrat
            tx = self.contract.functions.withdraw(self.web3.to_wei(amount_in_ether, "ether")).build_transaction({
                "from": self.sender_address,
                "gas": 200000,
                "gasPrice": current_gas_price + self.web3.to_wei(5, "gwei"),
                "nonce": self.web3.eth.get_transaction_count(self.sender_address),
            })
            # Signer la transaction
            signed_tx = self.web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            # Envoyer la transaction signée
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            transaction_logger.info(f"Withdrawal transaction sent with hash: {self.web3.to_hex(tx_hash)}")
            return tx_hash
        except Exception as e:
            error_logger.error(f"Error in withdraw_funds: {e}")
            raise