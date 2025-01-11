from blockchain.repository import BlockchainRepository
from logger import  error_logger
# La classe BlockchainService est une couche de service qui interagit avec le dépôt BlockchainRepository pour effectuer des transactions.
class BlockchainService:
    def __init__(self):
        # Initialisation de la classe BlockchainService.
        # Cette méthode crée une instance de BlockchainRepository pour interagir avec la blockchain.
        # Si une erreur survient lors de l'initialisation, elle est capturée et enregistrée dans les logs.
        try:
            # Création d'une instance de BlockchainRepository pour accéder aux fonctions de la blockchain.
            self.repository = BlockchainRepository()
        except Exception as e:
            # Si une erreur se produit, elle est enregistrée dans le log d'erreur.
            error_logger.error(f"Error initializing BlockchainService: {e}")
            raise

    def send_payment(self, amount_in_ether):
        #Envoie une transaction de paiement sur la blockchain.
        #Appelle la méthode send_transaction du BlockchainRepository pour envoyer de l'Ether au contrat.
        #Si une erreur survient, elle est capturée et enregistrée dans les logs.

        try:
            # Appel de la méthode send_transaction pour envoyer l'Ether au contrat.
            tx_hash = self.repository.send_transaction(amount_in_ether)
            # Retourner le hash de la transaction sous forme de chaîne hexadécimale.
            return tx_hash.hex()
        except Exception as e:
            # Si une erreur survient lors de l'envoi, elle est enregistrée dans les logs d'erreur.
            error_logger.error(f"Error in send_payment: {e}")
            raise

    def check_balance(self):
        #Vérifie le solde du contrat sur la blockchain.
        #Appelle la méthode get_balance du BlockchainRepository pour obtenir le solde du contrat.
        #Si une erreur survient, elle est capturée et enregistrée dans les logs.

        try:
            # Appel de la méthode get_balance pour récupérer le solde du contrat.
            balance = self.repository.get_balance()
            # Retourne le solde en Ether
            return balance
        except Exception as e:
            # Si une erreur survient lors de la récupération du solde, elle est enregistrée dans les logs d'erreur.
            error_logger.error(f"Error in check_balance: {e}")
            raise

    def withdraw_funds(self, amount_in_ether):
        #Effectue un retrait de fonds du contrat vers l'adresse de l'expéditeur.
        #Appelle la méthode withdraw_funds du BlockchainRepository pour initier le retrait.
        #Si une erreur survient, elle est capturée et enregistrée dans les logs.

        try:
            # Appel de la méthode withdraw_funds pour retirer des fonds du contrat.
            tx_hash = self.repository.withdraw_funds(amount_in_ether)
            # Retourne le hash de la transaction sous forme de chaîne hexadécimale.
            return tx_hash.hex()  # Retourne le hash de la transaction
        except Exception as e:
            # Si une erreur survient lors du retrait, elle est enregistrée dans les logs d'erreur.
            error_logger.error(f"Error in withdraw_funds: {e}")
            raise
