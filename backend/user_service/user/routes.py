from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import timedelta, datetime

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
from user.schema import WalletCreate, WalletRead
from user.services import WalletService

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
    """Register a new user with auto-generated defaults."""
    user_repository = UserRepository(session)

    # Check if the email is already registered
    existing_user = await user_repository.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    created_user = await user_repository.create_user(
        User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hashed_password,
            role="user",  # Default role
            disabled=False,  # Default disabled status
        )
    )

    return {
        "message": "User created successfully",
        "username": created_user.username,
        "user": created_user,
    }

@router.post("/admin/users", status_code=status.HTTP_201_CREATED)
async def create_user_by_admin(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Allow admins to create users with specific roles."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create users")

    user_repository = UserRepository(session)

    # Check if the email is already registered
    existing_user = await user_repository.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = hash_password(user.password)

    created_user = await user_repository.create_user(
        User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hashed_password,
            role="admin",  # Explicitly set the role
            disabled=False,  # Default disabled status

        )
    )

    return {
        "message": "Anew admin user has been created successfully",
        "user": created_user,
    }

@router.get("/admin/users/", response_model=list[UserRead])
async def get_all_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieve all users (admin or moderator access only)."""
    if current_user.role not in ["admin", "moderator"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await UserService.get_all_users(session)

@router.get("/admin/users/{user_id}", response_model=UserRead)
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
    updates = updated_user.dict(exclude_unset=True)
    if "password" in updates:
        updates["hashed_password"] = hash_password(updates.pop("password"))
    updated_user_obj = await UserService.update_user(session, current_user.username, updates)

    # Return the updated user data as a dictionary
    return updated_user_obj.dict()

@router.delete("/users/me", response_model=dict)
async def delete_current_user(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete the current user's account."""
    await UserService.delete_user(session, current_user.username)
    return {"message": "User account deleted successfully"}

@router.put("/admin/users/{username}/disable", status_code=status.HTTP_200_OK)
async def disable_user_account(
    username: str,
    disable: bool,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Enable or disable a user account (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can disable user accounts")

    user_repository = UserRepository(session)

    user = await user_repository.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.disabled = disable
    user.updated_at = datetime.utcnow()
    await session.commit()

    status_message = "disabled" if disable else "enabled"
    return {"message": f"User '{username}' has been {status_message}."}

@router.delete("/admin/users/{username}", status_code=status.HTTP_200_OK)
async def delete_user_by_admin(
    username: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Allow admins to delete a user."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete users")

    # Call the service to delete the user
    is_deleted = await UserService.delete_user(session, username)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User '{username}' has been deleted successfully."}

@router.post("/users/{username}/wallets", response_model=WalletRead)
async def create_wallet(
    username: str,
    wallet: WalletCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Create a wallet for the current user."""
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="You can only create wallets for yourself.")

    wallet_service = WalletService()

    # Create the wallet for the user, passing the correct username
    created_wallet = await wallet_service.create_wallet(session, username, wallet.currency, wallet.balance)

    return created_wallet
