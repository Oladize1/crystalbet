from pydantic import BaseModel, EmailStr
from typing import Optional

# User Creation Schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# User Login Schema
class UserLogin(BaseModel):
    username: str
    password: str

# User Response Schema
class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr

# Token Response Schema
class Token(BaseModel):
    access_token: str
    token_type: str
# Schema for the token data (to verify user info in the token)
class TokenData(BaseModel):
    email: Optional[str] = None