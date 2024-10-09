from fastapi import APIRouter, HTTPException, Depends, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from models.user import User  # Ensure this is your MongoDB user model
from schemas.user import UserCreate, UserLogin, UserResponse, Token, PasswordResetRequest, OTPVerification
from services.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    register_new_user,
    create_refresh_token,
    verify_refresh_token,
    send_verification_email,
    verify_email_token,
    send_reset_password_email,
    reset_user_password,
    send_otp,
    verify_otp
)
from datetime import timedelta
import os
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from passlib.context import CryptContext
from uuid import uuid4
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Set up logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Create a MongoDB client using the settings
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE_NAME")]
users_collection = db["users"]  
# Token expiration settings
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Multi-factor authentication (MFA) variables
failed_attempts = {}

# User Signup Model
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

# User signup route
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(user: UserSignup, background_tasks: BackgroundTasks):
    """
    Register a new user and send a verification email.
    """
    # Check if the username or email is already registered
    if await users_collection.find_one({"username": user.username}):
        logger.warning(f"Attempt to register with already taken username: {user.username}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    if await users_collection.find_one({"email": user.email}):
        logger.warning(f"Attempt to register with already taken email: {user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash the user's password and save the user data
    hashed_password = pwd_context.hash(user.password)
    new_user_data = user.dict()
    new_user_data["password"] = hashed_password
    new_user_data["is_verified"] = False  # Email verification status

    # Insert the new user into the database
    await users_collection.insert_one(new_user_data)

    # Send verification email
    verification_token = str(uuid4())
    background_tasks.add_task(send_verification_email, user.email, verification_token)

    logger.info(f"User {user.username} successfully registered. Verification email sent.")
    return new_user_data

# Email verification route
@router.get("/verify-email/{token}")
async def verify_email(token: str):
    """
    Endpoint to verify user's email.
    """
    user = await verify_email_token(token)
    if not user:
        logger.error("Email verification failed: Invalid or expired token")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    
    # Update the user's verification status in the database
    await users_collection.update_one({"_id": ObjectId(user["_id"])}, {"$set": {"is_verified": True}})
    logger.info(f"User {user['username']} verified their email.")
    return {"message": "Email verification successful"}

# Password reset request route
@router.post("/password-reset-request", status_code=status.HTTP_200_OK)
async def password_reset_request(email: EmailStr, background_tasks: BackgroundTasks):
    """
    Request a password reset link.
    """
    # Find the user by email
    user = await users_collection.find_one({"email": email})
    if not user:
        logger.warning(f"Password reset request failed: Email not found {email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    
    # Generate a password reset token and send the reset email
    reset_token = str(uuid4())
    background_tasks.add_task(send_reset_password_email, email, reset_token)
    
    logger.info(f"Password reset link sent to {email}")
    return {"message": "Password reset link sent"}

# Password reset route
@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(token: str, new_password: str):
    """
    Reset password using the provided token.
    """
    # Reset the user's password using the token
    user = await reset_user_password(token, new_password)
    if not user:
        logger.error("Password reset failed: Invalid or expired token")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    logger.info(f"User {user['username']} reset their password.")
    return {"message": "Password reset successful"}

# Send OTP for MFA route
@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_otp_request(current_user: User = Depends(get_current_active_user)):
    """
    Send OTP for MFA.
    """
    otp = await send_otp(current_user)
    if not otp:
        logger.error("Failed to send OTP")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send OTP")

    logger.info(f"OTP sent to user {current_user['username']}.")
    return {"message": "OTP sent"}

# Verify OTP route for MFA
@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp_code(otp: str, current_user: User = Depends(get_current_active_user)):
    """
    Verify OTP for MFA.
    """
    if not await verify_otp(current_user, otp):
        logger.warning(f"Invalid OTP attempt by user {current_user['username']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    
    logger.info(f"User {current_user['username']} verified OTP.")
    return {"message": "OTP verified"}

# Account locking mechanism for failed login attempts
failed_attempts = {}

# User login route with account locking after multiple failed attempts
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and issue a JWT token with account locking.
    """
    username = form_data.username
    password = form_data.password

    # Check if the account is temporarily locked
    if username in failed_attempts and failed_attempts[username] >= 5:
        logger.warning(f"Account temporarily locked for {username} due to too many failed attempts")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account temporarily locked due to too many failed login attempts")
    
    # Authenticate the user
    user = await authenticate_user(username, password)
    if not user:
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        logger.warning(f"Failed login attempt for {username}. Total failed attempts: {failed_attempts[username]}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    
    # Reset failed attempts after successful login
    if username in failed_attempts:
        del failed_attempts[username]

    # Create access and refresh tokens
    access_token = create_access_token(user["username"])
    refresh_token = create_refresh_token(user["username"])

    logger.info(f"User {user['username']} successfully logged in.")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
