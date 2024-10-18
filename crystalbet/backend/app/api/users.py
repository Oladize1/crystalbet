from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from typing import List
from db.mongodb import init_db

from services.user import get_user_profile, update_user_profile
from schemas.user import UserProfile, UserUpdate
from core.security import get_current_user

router = APIRouter()

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_user)):
    user = await get_user_profile(current_user["_id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/profile", response_model=UserProfile)
async def update_profile(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    updated_user = await update_user_profile(current_user["_id"], user_update)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user
