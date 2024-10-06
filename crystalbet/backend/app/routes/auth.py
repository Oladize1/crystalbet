from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from models.user import User  # Adjust the import according to your project structure
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    register_new_user,
)
from datetime import timedelta

router = APIRouter()

# User signup schema
class UserSignup(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    username: str = Field(..., min_length=3, description="Unique username with at least 3 characters")
    password: str = Field(..., min_length=6, description="Password with at least 6 characters")

    class Config:
        schema_extra = {
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
        schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepassword123"
            }
        }

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(user: UserSignup):
    """
    Endpoint to register a new user.
    """
    existing_user = await User.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    existing_email = await User.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = await register_new_user(user)
    return new_user

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to authenticate a user and return a JWT token.
    """
    authenticated_user = await authenticate_user(form_data.username, form_data.password)
    if not authenticated_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": authenticated_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to get the current authenticated user's details.
    """
    return current_user

@router.post("/logout")
async def logout_user():
    """
    Placeholder endpoint for logout functionality.
    """
    # Note: With JWT, logout is handled on the client side by deleting the token.
    return {"message": "Logout successful"}
