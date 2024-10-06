from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# Define an Enum for Payment Methods
class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit card"
    BANK_TRANSFER = "bank transfer"
    PAYPAL = "paypal"
    MOBILE_MONEY = "mobile money"

    def __str__(self):
        return self.value.capitalize()

# Define an Enum for Transaction Status
class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self):
        return self.value.capitalize()


# Schema for payment requests
class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0, description="The amount to deposit or withdraw, must be greater than 0")
    method: PaymentMethod = Field(..., description="Payment method used for the transaction")

    class Config:
        schema_extra = {
            "example": {
                "amount": 150.0,
                "method": "credit card"
            }
        }

# Schema for transaction responses
class TransactionResponse(BaseModel):
    message: str = Field(..., description="Message confirming the transaction outcome")
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    status: TransactionStatus = Field(..., description="Current status of the transaction")

    class Config:
        schema_extra = {
            "example": {
                "message": "Successfully deposited 150.0 via credit card",
                "transaction_id": "605c72ef3e3a2c35e563f91e",
                "status": "completed"
            }
        }
