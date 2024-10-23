# app/schemas/payment.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PaymentCreate(BaseModel):
    user_id: str
    amount: float
    currency: str

class PaymentResponse(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    amount: float
    currency: str
    status: str
    transaction_id: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True
        from_attributes = True
