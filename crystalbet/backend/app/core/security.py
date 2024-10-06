import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import MongoDBConnection  # Use MongoDBConnection class
from typing import Optional, Dict
from datetime import datetime, timedelta
import os  # For environment variable access

# Load JWT Secret and Config from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_default_jwt_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to hash a password securely
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Function to verify password matches stored hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# Function to create a JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode JWT and retrieve the current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    try:
        # Decode JWT and extract payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or credentials"
            )

        # Query user from database using MongoDBConnection class
        user = await MongoDBConnection.get_database()["users"].find_one({"username": username})
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# Function to check if a user has admin privileges
async def is_admin(user: dict = Depends(get_current_user)) -> bool:
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return True

# Role-based permission checker (supports multiple roles)
async def has_role(required_roles: list, user: dict = Depends(get_current_user)) -> bool:
    if user.get("role") not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the required permissions"
        )
    return True

# More general permission handling to allow role customization
async def check_permissions(user: dict = Depends(get_current_user), role: Optional[str] = None) -> bool:
    if role and user.get("role") != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required role: {role}"
        )
    return True
