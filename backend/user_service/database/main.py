from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from config import Config
import asyncio
from typing import AsyncGenerator

# Create the database engine
async_engine = create_async_engine(Config.DATABASE_URL, echo=True)

# Define sessionmaker globally
async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Initialize the database
async def init_db() -> None:
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

# Dependency to provide AsyncSession
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:  # Use async_session_factory to create the session
        yield session  # Yield the session to be used in the route
