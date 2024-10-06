import os
from core.config import settings  # Ensure settings is an instance, not a class
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import User  # Adjust based on your project structure
from schemas.user import UserCreate, TokenData
from typing import Optional

# Setup password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Utility to hash password
def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)

# Utility to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the given password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user by verifying password
async def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate user by username and password."""
    user = await User.find_one({"username": username})
    if user and verify_password(password, user.password):
        return user
    return None

# Register a new user
async def register_new_user(user_data: UserCreate) -> User:
    """Register a new user and save to the database."""
    if await User.find_one({"username": user_data.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if await User.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    await user.save()
    return user

# Create a JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Get the current active user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Retrieve the current active user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await User.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return user

# Get the current active user and verify
async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Ensure the current user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Function to create a refresh token
def create_refresh_token(data: dict) -> str:
    """
    Create a refresh token using the provided data.
    The token expires after a long period (e.g., 30 days).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    
    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return refresh_token

# Function to verify refresh token
def verify_refresh_token(token: str):
    """
    Verify the refresh token and return the payload data if valid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception