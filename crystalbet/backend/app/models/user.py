from pydantic import BaseModel, EmailStr, Field, ConfigDict
from bson import ObjectId

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: EmailStr
    full_name: str
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False

    class Config:
        json_encoders = {
            ObjectId: str
        }

# Helper function to transform BSON ObjectId to string when querying MongoDB
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "full_name": user["full_name"],
        "is_active": user["is_active"],
        "is_admin": user["is_admin"]
    }
