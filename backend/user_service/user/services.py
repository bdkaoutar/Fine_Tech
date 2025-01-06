from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from user.repository import UserRepository, WalletRepository
from user.model import User, Wallet


class UserService:
    @staticmethod
    async def create_user(
            session: AsyncSession, full_name: str, email: str, hashed_password: str
    ) -> User:
        """Create a new user and initialize wallets."""
        try:
            # Step 1: Create the user
            user_repository = UserRepository(session)  # Instantiate the UserRepository
            user = User(full_name=full_name, email=email, hashed_password=hashed_password)
            user = await user_repository.create_user(user)

            # Step 2: Delegate wallet creation to WalletService
            wallet_service = WalletService()  # Instantiate WalletService
            await wallet_service._create_default_wallets(session, user.username)  # Use `username` instead of `user.id`

            return user
        except Exception as e:
            # Rollback on failure
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
        """Update an existing user."""
        return await UserRepository.update_user(session, username, updates)

    @staticmethod
    async def delete_user(session: AsyncSession, username: str) -> bool:
        """Delete a user by their USERNAME."""
        return await UserRepository.delete_user(session, username)


class WalletService:
    @staticmethod
    async def create_wallet(session: AsyncSession, username: str, currency: str, balance: int) -> Wallet:
        """Create a new wallet for a user."""
        wallet = Wallet(username=username, currency=currency, balance=balance)
        return await WalletRepository(session).create_wallet(wallet)

    @staticmethod
    async def get_wallets_by_user(session: AsyncSession, username: str) -> List[Wallet]:
        """Fetch all wallets for a specific user."""
        return await WalletRepository.get_wallets_by_user(session, username)

    @staticmethod
    async def deposit_to_wallet(session: AsyncSession, wallet_id: int, amount: int) -> Optional[Wallet]:
        """Deposit money into a wallet."""
        return await WalletRepository.deposit_to_wallet(session, wallet_id, amount)

    @staticmethod
    async def _create_default_wallets(session: AsyncSession, username: str):
        """Create default wallets for a new user."""
        default_wallets = [
            Wallet(username=username, currency="USD", balance=0),
            Wallet(username=username, currency="EUR", balance=0),
        ]
        wallet_repository = WalletRepository(session)  # Instantiate WalletRepository
        for wallet in default_wallets:
            await wallet_repository.create_wallet(wallet)