from passlib.context import CryptContext
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from schemas.auth import UserCreate, UserOut, Token, TokenRefresh
from db.mongodb import get_db
import jwt
import os
from datetime import datetime, timedelta
from jwt.exceptions import PyJWTError

# OAuth2 password bearer scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        return None
    return User(**user)

async def register(user: UserCreate) -> UserOut:
    """Registers a new user, hashes their password, and stores them in the database."""
    user_dict = user.dict()

    # Check if the username already exists
    existing_user = await get_db().users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash password and prepare user data
    user_dict['hashed_password'] = hash_password(user.password)
    del user_dict['password']  # Remove the plain password before storing

    # Insert the new user into the database
    result = await get_db().users.insert_one(user_dict)
    user_dict['id'] = str(result.inserted_id)  # Store the generated ID
    return UserOut(**user_dict)

async def login(username: str, password: str) -> Token:
    """Authenticates a user and returns a JWT token if credentials are valid."""
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a JWT token with a 30-minute expiration
    token_data = {
        "sub": str(user["_id"]),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(token_data, os.getenv("SECRET_KEY"), algorithm="HS256")
    
    refresh_token_data = {
        "sub": str(user["_id"]),
        "exp": datetime.utcnow() + timedelta(days=30)  # Refresh token valid for 30 days
    }
    refresh_token = create_refresh_token(refresh_token_data)

    return Token(access_token=token, token_type="bearer", refresh_token=refresh_token)

def create_refresh_token(data: dict) -> str:
    """Creates a refresh token with an optional expiration."""
    to_encode = data.copy()
    token = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return token

def verify_refresh_token(token: str) -> str:
    """Verifies the refresh token and returns the user ID if valid."""
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return user_id
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate refresh token")

async def send_password_reset_email(email: str):
    """Sends a password reset email to the user."""
    user = await get_db().users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    # Logic for sending a password reset email goes here

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Decodes the JWT token and retrieves the current user."""
    try:
        # Decode the JWT token to extract user ID
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch the user from the database by user ID
        user = await get_db().users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return User(**user)

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Creates a JWT token with an optional expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)  # Default expiration time

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return token

async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> User:
    """Decodes the JWT token and retrieves the current active user."""
    return await get_current_user(token)  # Reuse get_current_user for this function

async def get_current_admin(token: str = Depends(oauth2_scheme)) -> User:
    """Decodes the JWT token and retrieves the current admin user."""
    user = await get_current_user(token)  # Reuse get_current_user for validation

    # Assuming there is a field in User model to check if the user is an admin
    if not user.is_admin:  # Replace with the actual field to check admin status
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return user
