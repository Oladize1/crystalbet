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
from fastapi_mail import FastMail, MessageSchema
import random

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
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=403, detail="Invalid password")

    return user

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
    """Create a refresh token using the provided data."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    
    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return refresh_token

# Function to verify refresh token
def verify_refresh_token(token: str):
    """Verify the refresh token and return the payload data if valid."""
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

# Function to send verification email
async def send_verification_email(email: str, otp: str):
    """Send a verification email with the OTP code."""
    message = MessageSchema(
        subject="Verify your account",
        recipients=[email],
        body=f"Your verification OTP is {otp}",
        subtype="html"
    )

    fm = FastMail(settings.EMAIL_CONFIG)
    await fm.send_message(message)

# Function to verify the email token
async def verify_email_token(token: str) -> bool:
    """Verify the email token and return whether it's valid."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Here you can add any additional logic for email verification if necessary
        return True  # Return True if token is valid
    except JWTError:
        raise credentials_exception

# Function to send reset password email
async def send_reset_password_email(email: str, otp: str):
    """Send a reset password email with the OTP code."""
    message = MessageSchema(
        subject="Reset your password",
        recipients=[email],
        body=f"Your reset password OTP is {otp}",
        subtype="html"
    )

    fm = FastMail(settings.EMAIL_CONFIG)
    await fm.send_message(message)

# Function to reset user password
async def reset_user_password(username: str, new_password: str) -> User:
    """Reset the user's password."""
    user = await User.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hash_password(new_password)
    user.password = hashed_password
    user.updated_at = datetime.utcnow()
    await user.save()
    return user

# Function to send OTP for various purposes
async def send_otp(email: str, purpose: str) -> str:
    """Send an OTP for verification or password reset."""
    otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP
    await send_verification_email(email, otp)  # You can replace this with send_reset_password_email based on the purpose
    return otp

# Function to verify OTP
async def verify_otp(input_otp: str, generated_otp: str) -> bool:
    """Verify the provided OTP against the generated OTP."""
    if input_otp != generated_otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return True
