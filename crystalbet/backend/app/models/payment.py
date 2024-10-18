from pydantic import BaseModel, Field, condecimal, constr
from bson import ObjectId
from datetime import datetime
from typing import Optional

# Custom ObjectId type for Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class Payment(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    amount: condecimal(gt=0)  # Use condecimal to ensure positive amounts
    currency: constr(min_length=3, max_length=3)  # Currency code (e.g., USD, EUR)
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for JSON serialization
        }

# Example usage
if __name__ == "__main__":
    payment_example = Payment(
        user_id="user_123",
        amount=100.50,
        currency="USD",
        status="completed",
        transaction_id="txn_456"
    )

    print(payment_example.json())  # Serialize to JSON
