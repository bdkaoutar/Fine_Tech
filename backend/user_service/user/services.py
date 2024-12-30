from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repository import UserRepository
from model import User


class UserService:
    @staticmethod
    async def create_user(session: AsyncSession, name: str, email: str, hashed_password: str) -> User:
        user = User(name=name, email=email, hashed_password=hashed_password)
        return await UserRepository.create_user(session, user)

    @staticmethod
    def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        return UserRepository.get_user_by_id(session, user_id)

    @staticmethod
    def get_all_users(session: AsyncSession) -> List[User]:
        return UserRepository.get_all_users(session)

    @staticmethod
    def update_user(session: AsyncSession, user_id: int, updates: dict) -> Optional[User]:
        return UserRepository.update_user(session, user_id, updates)

    @staticmethod
    def delete_user(session: AsyncSession, user_id: int) -> bool:
        return UserRepository.delete_user(session, user_id)
