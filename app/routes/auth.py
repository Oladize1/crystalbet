from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.auth import login, signup, get_user, logout

router = APIRouter()

class UserSignup(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def create_user(user: UserSignup):
    return await signup(user)

@router.post("/login")
async def login_user(user: UserLogin):
    return await login(user)

@router.get("/user/{user_id}")
async def read_user(user_id: str):
    return await get_user(user_id)

@router.post("/logout")
async def logout_user():
    return await logout()
