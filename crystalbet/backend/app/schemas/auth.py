from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Existing UserCreate schema
class UserCreate(BaseModel):
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="strongpassword123")

# Existing UserOut schema for output
class UserOut(BaseModel):
    id: str = Field(..., example="60d5ec49f22b2c001c9a5c01")  # Example ObjectId as string
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="john.doe@example.com")

# Existing Token schema
class Token(BaseModel):
    access_token: str = Field(..., example="your_access_token_here")
    token_type: str = Field(default="Bearer", example="Bearer")  # Default type is Bearer
    refresh_token: Optional[str] = Field(None, example="your_refresh_token_here")  # Optional refresh token

# Existing TokenRefresh schema
class TokenRefresh(BaseModel):
    refresh_token: str = Field(..., example="your_refresh_token_here")  # Required field for refresh token request

# Schema for requesting a password reset (step 1 - requesting the token)
class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")  # User's email for password reset

# Schema for resetting the password (step 2 - actual password reset)
class PasswordReset(BaseModel):
    reset_token: str = Field(..., example="your_reset_token_here")  # Reset token provided by the system
    new_password: str = Field(..., example="newStrongPassword123")  # New password chosen by the user
    confirm_password: str = Field(..., example="newStrongPassword123")  # Confirmation of the new password

    # Validation to ensure both passwords match
    @staticmethod
    def validate_passwords(values: dict) -> dict:
        new_password = values.get('new_password')
        confirm_password = values.get('confirm_password')
        if new_password != confirm_password:
            raise ValueError("Passwords do not match")
        return values

    class Config:
        schema_extra = {
            "example": {
                "reset_token": "your_reset_token_here",
                "new_password": "newStrongPassword123",
                "confirm_password": "newStrongPassword123"
            }
        }

# Schema for updating user profile (UserUpdate)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, example="john_doe_updated")
    email: Optional[EmailStr] = Field(None, example="john.doe_updated@example.com")
    full_name: Optional[str] = Field(None, example="John Doe Updated")
    password: Optional[str] = Field(None, example="newStrongPassword123")
    is_active: Optional[bool] = Field(None, example=True)
    
    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe_updated",
                "email": "john.doe_updated@example.com",
                "full_name": "John Doe Updated",
                "password": "newStrongPassword123",
                "is_active": True
            }
        }
