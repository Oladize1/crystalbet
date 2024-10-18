from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str  # Include refresh_token in the Token response

class TokenRefresh(BaseModel):
    refresh_token: str  # Schema for the refresh token request
