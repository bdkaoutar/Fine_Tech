from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from user.repository import UserRepository, WalletRepository
from user.model import User, Wallet
from fastapi import HTTPException

class UserService:
    @staticmethod
    async def create_user(
            session: AsyncSession, full_name: str, email: str, hashed_password: str
    ) -> User:
        """Create a new user and initialize wallets."""
        try:
            # Step 1: Create the user
            user_repository = UserRepository(session)
            user = User(full_name=full_name, email=email, hashed_password=hashed_password)
            user = await user_repository.create_user(user)

            print(f"User {user.username} created. Now creating default wallets.")  # Log here

            return user
        except Exception as e:
            await session.rollback()
            raise RuntimeError(f"Error creating user: {e}")


    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
        """Fetch a user by USERNAME."""
        user_repository = UserRepository(session)
        return await user_repository.get_user_by_username(username)

    @staticmethod
    async def get_all_users(session: AsyncSession) -> List[User]:
        """Fetch all users."""
        user_repository = UserRepository(session)
        return await user_repository.get_all_users()

    @staticmethod
    async def update_user(session: AsyncSession, username: str, updates: dict) -> Optional[User]:
        user_repository = UserRepository(session)  # Ensure session is properly passed here
        return await user_repository.update_user(username, updates)


    @staticmethod
    async def delete_user(session: AsyncSession, username: str) -> bool:
        user_repository = UserRepository(session)  # Ensure session is passed correctly
        return await user_repository.delete_user(username)


class WalletService:
    @staticmethod
    async def create_wallet(session: AsyncSession, username: str, currency: str, balance: int) -> Wallet:
        """Create a new wallet for the user."""
        if username is None:
            raise HTTPException(status_code=400, detail="Username cannot be None")  # Added validation for username

        # Ensure username is passed and assigned to wallet
        wallet = Wallet(username=username, currency=currency, balance=balance)
        created_wallet = await WalletRepository(session).create_wallet(wallet)

        # Log the wallet creation process to track what is happening
        print(f"Wallet created for user {username}: {wallet.currency} with balance {wallet.balance}")
        return created_wallet
    @staticmethod
    async def get_wallets_by_user(session: AsyncSession, username: str) -> List[Wallet]:
        """Fetch all wallets for a specific user."""
        return await WalletRepository.get_wallets_by_user(session, username)

    @staticmethod
    async def deposit_to_wallet(session: AsyncSession, wallet_id: int, amount: int) -> Optional[Wallet]:
        """Deposit money into a wallet."""
        return await WalletRepository.deposit_to_wallet(session, wallet_id, amount)

    async def _create_default_wallets(session: AsyncSession, username: str):
        """Create default wallets for a new user."""
        print(f"Creating default wallets for {username}")  # Add logging
        default_wallets = [
            Wallet(username=username, currency="USD", balance=0),
            Wallet(username=username, currency="EUR", balance=0),
        ]
        wallet_repository = WalletRepository(session)
        for wallet in default_wallets:
            await wallet_repository.create_wallet(wallet)
            print(f"Created wallet {wallet.currency} for {username}")  # Log each wallet creation
