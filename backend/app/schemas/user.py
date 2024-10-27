from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Schema for returning user profile details
class UserProfile(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

# Schema for updating the user profile
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

# Schema for creating a new user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for returning user details in response
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

# Schema for returning authentication tokens
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
