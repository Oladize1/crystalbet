from pydantic import BaseModel, EmailStr, Field, ConfigDict
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId class for Pydantic."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    hashed_password: str

    # Pydantic v2: Use model_config with ConfigDict
    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Allow ObjectId as a custom type
        json_encoders={ObjectId: str}  # Convert ObjectId to string in JSON responses
    )

# Example usage
user = User(username="johndoe", email="johndoe@example.com", hashed_password="hashed_pass")
print(user.json())  # {"_id": "<some ObjectId as string>", "username": "johndoe", "email": "johndoe@example.com"}
