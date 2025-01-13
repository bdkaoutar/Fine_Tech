import logging
import os

# Ensure the logs folder exists
os.makedirs("scripts/logs", exist_ok=True)

# Error logger configuration
error_logger = logging.getLogger("error_logger")
error_handler = logging.FileHandler("scripts/logs/error_logs.log")
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_formatter)
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)

# Transaction logger configuration
transaction_logger = logging.getLogger("transaction_logger")
transaction_handler = logging.FileHandler("scripts/logs/transaction_logs.log")
transaction_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
transaction_handler.setFormatter(transaction_formatter)
transaction_logger.setLevel(logging.INFO)
transaction_logger.addHandler(transaction_handler)