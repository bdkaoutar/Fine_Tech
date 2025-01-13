import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
