from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Schema for returning user profile details
class UserProfile(BaseModel):
    id: str = Field(..., alias="_id")  # Using alias for MongoDB ObjectId
    email: EmailStr
    full_name: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True
        populate_by_name = True  # Allows using field names directly

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
    id: str = Field(..., alias="_id")  # Using alias for MongoDB ObjectId
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True
        populate_by_name = True  # Allows using field names directly

# Schema for returning authentication tokens
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data, to be included in the request/response of secured routes
class TokenData(BaseModel):
    email: Optional[EmailStr] = None

# Schema for the user stored in the database
class UserInDB(UserResponse):
    hashed_password: str  # The hashed password stored in the database

    class Config:
        from_attributes = True
        populate_by_name = True  # Allows using field names directly
