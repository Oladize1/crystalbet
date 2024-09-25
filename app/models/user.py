# app/models/user.py
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"  # Default to regular user

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(User):
    pass
