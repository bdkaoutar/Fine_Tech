from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import Config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import get_session
from user.model import User
from user.schema import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + (expires_delta or timedelta(minutes=15))})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


# Get the current user from the JWT token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch the user from the database
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user


# Ensure the user is active and not disabled
async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
