# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from .env file

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
