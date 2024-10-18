from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import UserCreate, UserOut, Token
from services.auth import register, login, send_password_reset_email  # Importing refactored functions

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    """Register a new user."""
    return await register(user)

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login a user and return a JWT token."""
    return await login(form_data.username, form_data.password)

@router.post("/password-reset")
async def password_reset(email: str):
    """Send a password reset email."""
    await send_password_reset_email(email)
    return {"message": "Password reset email sent."}
