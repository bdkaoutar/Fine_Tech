from datetime import datetime
from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model import User


class UserRepository:
    @staticmethod
    async def create_user(session: AsyncSession, user: User) -> User:
        """Create a new user."""
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        """Fetch a user by their ID."""
        return await session.get(User, user_id)

    @staticmethod
    async def get_all_users(session: AsyncSession) -> List[User]:
        """Fetch all users."""
        result = await session.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, updates: dict) -> Optional[User]:
        """Update an existing user with the given updates."""
        user = await session.get(User, user_id)
        if user:
            for key, value in updates.items():
                setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            await session.commit()
            await session.refresh(user)
        return user

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int) -> bool:
        """Delete a user by their ID."""
        user = await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False
