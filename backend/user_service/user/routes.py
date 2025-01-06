from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import timedelta

from database.main import get_session
from user.model import User
from user.schema import UserCreate, UserRead, UserBase, Token, UserUpdateProfile
from utils.auth import (
    create_access_token, verify_password, hash_password,
    get_current_active_user
)
from config import Config
from user.services import UserService
from user.repository import UserRepository

router = APIRouter()

# General Routes
@router.get("/")
async def root():
    return {"message": "Welcome to the User Management Service!"}

@router.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}

# Authentication Routes

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Authenticate a user and return an access token."""
    query = select(User).where(User.username == form_data.username)
    user = (await session.execute(query)).scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
# User Management Routes
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    """Register a new user."""
    try:
        # Check for existing username and email
        user_repository = UserRepository(session)
        existing_user_by_username = await user_repository.get_user_by_username(user.username)
        if existing_user_by_username:
            raise HTTPException(status_code=400, detail="Username already exists")

        existing_user_by_email = await user_repository.get_user_by_email(user.email)
        if existing_user_by_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password and create the user
        hashed_password = hash_password(user.password)
        created_user = await UserService.create_user(
            session=session,
            full_name=user.full_name,
            email=user.email,
            hashed_password=hashed_password,
        )
        return {"message": "User created successfully", "user": created_user}
    except HTTPException as e:
        raise e
    except Exception as e:
        await session.rollback()  # Rollback on failure
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def admin_create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Allow admins to create a new user."""
    try:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Only admins can create users")

        # Check for existing username and email
        user_repository = UserRepository(session)
        existing_user_by_username = await user_repository.get_user_by_username(user.username)
        if existing_user_by_username:
            raise HTTPException(status_code=400, detail="Username already exists")

        existing_user_by_email = await user_repository.get_user_by_email(user.email)
        if existing_user_by_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password and create the user
        hashed_password = hash_password(user.password)
        created_user = await UserService.create_user(
            session=session,
            full_name=user.full_name,
            email=user.email,
            hashed_password=hashed_password,
        )
        return {"message": "User created successfully", "user": created_user}
    except HTTPException as e:
        raise e
    except Exception as e:
        await session.rollback()  # Rollback in case of failure
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/users/", response_model=list[UserRead])
async def get_all_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieve all users (admin or moderator access only)."""
    if current_user.role not in ["admin", "moderator"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await UserService.get_all_users(session)

@router.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieve a user by their ID (admin or moderator access only)."""
    if current_user.role not in ["admin", "moderator"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    user = await UserService.get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/me", response_model=dict)
async def update_current_user(
    updated_user: UserUpdateProfile,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update the current user's profile."""
    updated_user_data = updated_user.dict(exclude_unset=True)
    if "password" in updated_user_data:
        updated_user_data["hashed_password"] = hash_password(updated_user_data.pop("password"))
    return await UserService.update_user(session, current_user.username, updated_user_data)

@router.delete("/users/me", response_model=dict)
async def delete_current_user(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete the current user's account."""
    await UserService.delete_user(session, current_user.username)
    return {"message": "User account deleted successfully"}