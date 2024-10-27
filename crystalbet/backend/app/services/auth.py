from bson import ObjectId
from fastapi import HTTPException, status, Depends
from pydantic import EmailStr
from datetime import datetime, timedelta
from schemas.auth import UserCreate, UserUpdate
from models.user import UserInDB
from core.security import hash_password, verify_password, create_access_token, create_reset_token
from fastapi_mail import FastMail, MessageSchema
from db.mongodb import get_db
from core.config import settings
from utils.jwt import decode_token, oauth2_scheme  # Correct import for JWT functions

# Create a new user
async def create_user(db, user: UserCreate):
    # Check if the email is already registered
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )
    
    # Hash the password and prepare user data
    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True,
        "is_superuser": False,
    }
    result = await db["users"].insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)  # Add inserted ID for returning
    return UserInDB(**user_data)

# Authenticate a user by email and password
async def authenticate_user(db, email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return UserInDB(**user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password."
    )

# Send password reset email
async def send_reset_password_email(email: EmailStr, db):
    user = await db["users"].find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found."
        )

    token = create_reset_token({"email": email})
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"Click the following link to reset your password: {reset_link}",
        subtype="html"
    )
    
    # Send email
    fm = FastMail(settings.mail_config)
    await fm.send_message(message)
    
    # Save reset token and expiration
    await db["users"].update_one(
        {"email": email},
        {"$set": {"reset_token": token, "reset_token_expiration": datetime.utcnow() + timedelta(hours=1)}}
    )

# Reset user password
async def reset_password(db, reset_token: str, new_password: str):
    user = await db["users"].find_one({"reset_token": reset_token})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid reset token."
        )
    
    if user["reset_token_expiration"] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired."
        )
    
    # Hash the new password and update user document
    hashed_password = hash_password(new_password)
    await db["users"].update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {"password": hashed_password, "reset_token": None, "reset_token_expiration": None}}
    )

async def get_user_by_email(db, email: EmailStr):
    user = await db["users"].find_one({"email": email})
    if user:
        return UserInDB(**user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with this email not found."
    )

# Update user details
async def update_user(db, user_update: UserUpdate, user_id: str):
    # Validate user ID
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID."
        )
    
    # Find user by ID
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Prepare the update data
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])  # Hash the new password
    
    # Update user in the database
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    
    # Return the updated user
    updated_user = await db["users"].find_one({"_id": ObjectId(user_id)})
    return UserInDB(**updated_user)

# Verify admin privileges
async def verify_admin(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    user_info = await decode_token(token)
    user = await db["users"].find_one({"_id": ObjectId(user_info["sub"])})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    if not user.get("is_superuser", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )
    
    return UserInDB(**user)


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        # Decode the JWT token to extract user information
        user_info = decode_token(token)
        user_id = user_info.get("sub")

        # Retrieve the user from the database
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        return UserInDB(**user)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )