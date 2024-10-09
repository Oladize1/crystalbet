from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from services.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    register_new_user,
    create_refresh_token,
    verify_refresh_token,
)
from datetime import timedelta
import os
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from passlib.context import CryptContext

router = APIRouter()
logger = logging.getLogger(__name__)

# Configurable token expiration (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Limiter for rate limiting
limiter = Limiter(key_func=get_remote_address)

# User signup schema
class UserSignup(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    username: str = Field(..., min_length=3, description="Unique username with at least 3 characters")
    password: str = Field(..., min_length=6, description="Password with at least 6 characters")

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "username": "john_doe",
                "password": "securepassword123"
            }
        }

# Hashing password utility function
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# User Signup Route with password hashing
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(user: UserSignup):
    """
    Endpoint to register a new user.
    """
    existing_user = await User.find_one({"username": user.username})
    if existing_user:
        logger.warning(f"Attempt to register with already taken username: {user.username}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    existing_email = await User.find_one({"email": user.email})
    if existing_email:
        logger.warning(f"Attempt to register with already taken email: {user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash the password before saving the user
    hashed_password = hash_password(user.password)
    new_user_data = user.dict()
    new_user_data["password"] = hashed_password  # Store hashed password
    
    new_user = await register_new_user(new_user_data)
    logger.info(f"User {user.username} successfully registered.")
    return new_user

# User login with JWT and rate limiting
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to authenticate a user and return a JWT token.
    """
    authenticated_user = await authenticate_user(form_data.username, form_data.password)
    if not authenticated_user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.username}, expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(authenticated_user.username, expires_days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    logger.info(f"User {form_data.username} logged in successfully.")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Refresh Token Endpoint
@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str):
    """
    Endpoint to refresh access token using refresh token.
    """
    username = verify_refresh_token(refresh_token)
    if not username:
        logger.warning("Invalid refresh token attempt.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    
    logger.info(f"Access token refreshed for user {username}.")
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user information
@router.get("/user/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to get the current authenticated user's details.
    """
    logger.info(f"Current user data accessed: {current_user.username}")
    return current_user

# User Logout Endpoint
@router.post("/logout")
async def logout_user():
    """
    Placeholder endpoint for logout functionality.
    """
    logger.info("User logged out.")
    # Note: With JWT, logout is handled on the client side by deleting the token.
    return {"message": "Logout successful"}
