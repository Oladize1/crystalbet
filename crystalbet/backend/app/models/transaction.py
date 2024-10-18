# models/transaction.py
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # MongoDB ObjectId
    user_id: str
    amount: float
    status: str  # e.g., 'completed', 'pending', 'failed'
    created_at: str

    class Config:
        allow_population_by_field_name = True
