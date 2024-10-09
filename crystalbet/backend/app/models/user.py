#models/user.py
from pydantic import BaseModel, Field, EmailStr
from beanie import Document
from datetime import datetime

class User(Document):
    username: str = Field(..., description="Unique username for the user", index=True)  # Indexed directly in Field
    email: EmailStr = Field(..., description="User's email address", index=True, unique=True)
    password: str = Field(..., description="Hashed password for the user account")
    role: str = Field(default="user", description="Role of the user, default is 'user'")
    is_active: bool = Field(default=True, description="Whether the user's account is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "users"  # MongoDB collection name

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "hashed_password",
                "role": "user",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }

# Example to initialize the User model
async def create_user_index():
    await User.init_index()
