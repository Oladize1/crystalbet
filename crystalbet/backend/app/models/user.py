from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    username: str = Field(..., description="Unique username for the user")
    password: str = Field(..., min_length=6, description="Password for the user account (minimum 6 characters)")
    email: EmailStr = Field(..., description="User's email address")
    role: str = Field("user", description="Role of the user, default is 'user'")

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepassword",
                "email": "john@example.com",
                "role": "user"
            }
        }

class LoginRequest(BaseModel):
    username: str = Field(..., description="Username of the user trying to log in")
    password: str = Field(..., description="Password for the user account")

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepassword"
            }
        }

class RegisterRequest(User):
    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepassword",
                "email": "john@example.com",
                "role": "user"
            }
        }
