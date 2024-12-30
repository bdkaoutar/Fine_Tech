from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session
from backend.user_service.database.main import get_session
from schema import UserCreate, UserRead
from services import UserService
from model import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    # Check if the email already exists
    existing_users: List[User] = await UserService.get_all_users(session)
    if any(u.email == user_data.email for u in existing_users):
        raise HTTPException(status_code=400, detail="Email already in use.")

    # Create a new user
    return await UserService.create_user(session, user_data.name, user_data.email, user_data.hashed_password)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = UserService.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.get("/", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    return UserService.get_all_users(session)


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, updates: dict, session: Session = Depends(get_session)):
    user = UserService.update_user(session, user_id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    success = UserService.delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"message": "User deleted successfully."}
