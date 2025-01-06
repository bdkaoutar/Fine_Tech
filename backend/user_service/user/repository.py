
from datetime import datetime
from pydantic import EmailStr
from typing import List, Optional
from sqlmodel import select, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from user.model import User, Wallet

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User:
        """Create a new user."""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Fetch a user by their USERNAME."""
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        """Fetch a user by their EMAIL."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_all_users(self) -> List[User]:
        """Fetch all users."""
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def update_user(self, username: str, updates: dict) -> Optional[User]:
        """Update an existing user with the given updates."""
        user = await self.session.get(User, username)
        if user:
            for key, value in updates.items():
                setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def delete_user(self, username: str) -> bool:
        """Delete a user by their ID."""
        user = await self.session.get(User, username)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False

class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_wallet(self, wallet: Wallet) -> Wallet:
        """Create a new wallet."""
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet

    async def get_wallets_by_user(self, username: str) -> List[Wallet]:
        """Fetch all wallets of a user."""
        result = await self.session.execute(select(Wallet).where(Wallet.username == username))
        return result.scalars().all()

    async def deposit_to_wallet(self, wallet_id: int, amount: int) -> Optional[Wallet]:
        """Deposit money to a wallet."""
        wallet = await self.session.get(Wallet, wallet_id)
        if wallet:
            wallet.balance += amount
            await self.session.commit()
            await self.session.refresh(wallet)
        return wallet