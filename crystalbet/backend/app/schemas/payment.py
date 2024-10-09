# schemas/payment.py

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class InitiatePaymentSchema(BaseModel):
    user_id: str
    amount: float
    payment_method: str
    description: Optional[str] = None

class ConfirmPaymentSchema(BaseModel):
    user_id: str
    transaction_id: str
    payment_status: str

class PaymentHistorySchema(BaseModel):
    transaction_id: str
    amount: float
    payment_method: str
    payment_status: str
    timestamp: str

class PaymentResponseModel(BaseModel):
    message: str
    data: Dict[str, Any]

class ErrorResponseModel(BaseModel):
    detail: str
