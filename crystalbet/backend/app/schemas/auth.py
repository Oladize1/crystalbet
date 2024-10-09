from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Token response schema
class Token(BaseModel):
    access_token: str
    token_type: str

# User registration schema
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    username: str = Field(..., min_length=3, description="Unique username with at least 3 characters")
    password: str = Field(..., min_length=6, description="Password with at least 6 characters")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "username": "john_doe",
                "password": "securepassword123"
            }
        }

# User login schema
class UserLogin(BaseModel):
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepassword123"
            }
        }

# User response schema
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123456",
                "email": "john.doe@example.com",
                "username": "john_doe"
            }
        }
