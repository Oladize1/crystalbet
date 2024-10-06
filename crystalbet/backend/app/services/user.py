from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException, Depends
from models.user import UserSchema, UserUpdateSchema, UserLoginSchema
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from core.config import settings

# Database setup
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["betting_db"]
users_collection = db["users"]

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token creation
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Helper function for hashing passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper function for verifying passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Helper function for creating JWT tokens
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Register a new user
async def register_user(user_data: UserSchema):
    try:
        user_dict = user_data.dict()
        user_dict["password"] = hash_password(user_dict["password"])

        # Check if email already exists
        existing_user = await users_collection.find_one({"email": user_dict["email"]})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        result = await users_collection.insert_one(user_dict)
        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {str(e)}")

# Authenticate and login a user
async def login_user(login_data: UserLoginSchema):
    try:
        user = await users_collection.find_one({"email": login_data.email})
        if not user or not verify_password(login_data.password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": user["email"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging in: {str(e)}")

# Fetch user profile by user ID
async def fetch_user(user_id: str):
    try:
        user = await users_collection.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

# Update user profile
async def update_user(user_id: str, user_update_data: UserUpdateSchema):
    try:
        update_data = user_update_data.dict(exclude_unset=True)

        # If password is being updated, hash it
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        result = await users_collection.update_one({"_id": user_id}, {"$set": update_data})
        if result.modified_count == 1:
            return {"message": "User updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found or no changes made")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

# Delete a user by ID
async def delete_user(user_id: str):
    try:
        result = await users_collection.delete_one({"_id": user_id})
        if result.deleted_count == 1:
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")

# Reset password (assume some OTP or verification process in place)
async def reset_password(email: str, new_password: str):
    try:
        user = await users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        hashed_password = hash_password(new_password)
        result = await users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
        if result.modified_count == 1:
            return {"message": "Password reset successfully"}
        else:
            raise HTTPException(status_code=404, detail="Password reset failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting password: {str(e)}")

# Fetch all users (for admin purposes)
async def fetch_all_users():
    try:
        users = await users_collection.find().to_list(length=None)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all users: {str(e)}")
