from passlib.context import CryptContext
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from schemas.auth import UserCreate, UserOut, Token
from db.mongodb import get_db
import jwt
import os
from datetime import datetime, timedelta
from jwt.exceptions import PyJWTError
import logging

# Configure logger
logger = logging.getLogger(__name__)

# OAuth2 password bearer scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ensure SECRET_KEY is set
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise ValueError("No SECRET_KEY set for JWT encoding/decoding.")

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def hash_password(password: str) -> str:
    """Hashes the plain password."""
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str) -> User:
    """Authenticates a user by checking username and password."""
    user = await get_db().users.find_one({"username": username})
    if not user or not verify_password(password, user['hashed_password']):
        logger.warning("Authentication failed for user: %s", username)
        return None
    return User(**user)

async def register(user: UserCreate) -> UserOut:
    """Registers a new user, hashes their password, and stores them in the database."""
    user_dict = user.dict()
    
    # Check if the username already exists
    existing_user = await get_db().users.find_one({"username": user.username})
    if existing_user:
        logger.warning("Registration failed: Username already registered - %s", user.username)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User registration failed")

    # Hash password and prepare user data
    user_dict['hashed_password'] = hash_password(user.password)
    del user_dict['password']  # Remove the plain password before storing

    # Insert the new user into the database
    result = await get_db().users.insert_one(user_dict)
    user_dict['id'] = result.inserted_id  # Store the generated ID
    logger.info("User registered successfully: %s", user.username)
    return UserOut(**user_dict)

async def login(username: str, password: str) -> Token:
    """Authenticates a user and returns a JWT token if credentials are valid."""
    user = await authenticate_user(username, password)
    if not user:
        logger.warning("Login failed for user: %s", username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create a JWT token with a 30-minute expiration
    token_data = {
        "sub": str(user["_id"]),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    logger.info("User logged in successfully: %s", username)
    return Token(access_token=token, token_type="bearer")

async def send_password_reset_email(email: str):
    """Sends a password reset email to the user."""
    user = await get_db().users.find_one({"email": email})
    if not user:
        logger.warning("Password reset requested for non-existent email: %s", email)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    # Logic for sending a password reset email goes here
    logger.info("Password reset email sent to: %s", email)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Decodes the JWT token and retrieves the current user."""
    try:
        # Decode the JWT token to extract user ID
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            logger.warning("Invalid token: No user ID found.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Fetch the user from the database by user ID
        user = await get_db().users.find_one({"_id": ObjectId(user_id)})
        if not user:
            logger.warning("User not found for ID: %s", user_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return User(**user)

    except PyJWTError:
        logger.error("Token validation failed.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Creates a JWT token with an optional expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)  # Default expiration time

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return token

async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> User:
    """Decodes the JWT token and retrieves the current active user."""
    return await get_current_user(token)  # Reuse get_current_user for this function
