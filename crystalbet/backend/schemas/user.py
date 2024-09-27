# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field

# Define LoginRequest schema
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
            }
        }

# Define RegisterRequest schema
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

    class Config:
        schema_extra = {
            "example": {
                "username": "user123",
                "email": "user@example.com",
                "password": "strongpassword123",
            }
        }
