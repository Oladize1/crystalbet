from typing import Optional
from pydantic import BaseModel, Field

# Define the TransactionSchema for a transaction
class TransactionSchema(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    amount: float = Field(..., gt=0, description="Amount involved in the transaction")
    method: str = Field(..., description="Method of payment (e.g., 'credit_card', 'paypal')")
    status: str = Field(..., description="Current status of the transaction")

    class Config:
        schema_extra = {
            "example": {
                "transaction_id": "txn_123456",
                "amount": 50.0,
                "method": "credit_card",
                "status": "completed"
            }
        }

# Define the TransactionUpdateSchema for updating transaction information
class TransactionUpdateSchema(BaseModel):
    amount: Optional[float] = Field(None, gt=0, description="Updated amount for the transaction")
    status: Optional[str] = Field(None, description="Updated status of the transaction")

    class Config:
        schema_extra = {
            "example": {
                "amount": 60.0,
                "status": "pending"
            }
        }

# Your existing PaymentRequest and PaymentResponse classes should remain as defined
class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to be processed for the payment")
    method: str = Field(..., description="Payment method (e.g., 'credit_card', 'paypal')")

    class Config:
        schema_extra = {
            "example": {
                "amount": 50.0,
                "method": "credit_card"
            }
        }

class PaymentResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the payment was successful")
    transaction_id: Optional[str] = Field(None, description="Unique ID of the payment transaction")
    message: Optional[str] = Field(None, description="Message regarding the transaction")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "transaction_id": "txn_123456",
                "message": "Payment processed successfully."
            }
        }
