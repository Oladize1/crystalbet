from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError, ConfigDict
from typing import Optional
from models.user import User  # Ensure you have a User model to fetch user data from DB
from schemas.auth import TokenData  # Assuming TokenData schema validates JWT token claims
from core.config import settings  # Assuming settings.py contains secret key and algorithm configs
import bcrypt

# OAuth2 scheme to get the token from the "Authorization" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# JWT Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Create an access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify and decode the access token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    return token_data

class JWTBearer:
    def __init__(self, scopes: SecurityScopes = None):
        self.scopes = scopes

    async def __call__(self, request: Request, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload  # Store the payload in request.state.user
        except JWTError:
            raise credentials_exception
        
        # If scopes are used, you can validate them here
        if self.scopes and "scope" not in payload:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Dependency to retrieve the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    
    user = User.get_user_by_username(token_data.username)  # Ensure you implement this method
    if user is None:
        raise credentials_exception
    
    return user

def hash_password(password: str) -> str:
    """Hashes the password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies the password against the hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Refresh token logic can be added similarly by creating another function for long-term sessions
