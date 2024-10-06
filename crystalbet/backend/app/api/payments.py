from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.payment import (
    initiate_payment,
    confirm_payment,
    fetch_payment_history,
)
import logging

router = APIRouter()

# Initialize logger for this module
logger = logging.getLogger("payment_routes")

# Response models
class PaymentResponseModel(BaseModel):
    message: str
    data: Dict[str, Any]

class ErrorResponseModel(BaseModel):
    detail: str

# Define payment schemas (as per the service requirements)
class InitiatePaymentSchema(BaseModel):
    user_id: str
    amount: float
    payment_method: str
    description: Optional[str] = None

class ConfirmPaymentSchema(BaseModel):
    user_id: str
    transaction_id: str
    payment_status: str  # Consider using Enum for status

class PaymentHistorySchema(BaseModel):
    transaction_id: str
    amount: float
    payment_method: str
    payment_status: str
    timestamp: str

# Routes for payment operations

@router.post("/initiate-payment", response_model=PaymentResponseModel, status_code=status.HTTP_201_CREATED)
async def initiate_payment_route(payment_details: InitiatePaymentSchema):
    """
    Initiates a new payment.
    """
    try:
        logger.info(f"Initiating payment: {payment_details}")
        result = await initiate_payment(payment_details.dict())  # Convert Pydantic model to dict
        return {"message": "Payment initiated successfully", "data": result}
    except Exception as e:
        logger.error(f"Error while initiating payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while initiating the payment."
        )

@router.post("/confirm-payment", response_model=PaymentResponseModel, status_code=status.HTTP_200_OK)
async def confirm_payment_route(payment_details: ConfirmPaymentSchema):
    """
    Confirms the payment status.
    """
    try:
        logger.info(f"Confirming payment: {payment_details}")
        result = await confirm_payment(payment_details.transaction_id)  # Use transaction_id for confirmation
        return {"message": "Payment confirmed successfully", "data": result}
    except Exception as e:
        logger.error(f"Error while confirming payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while confirming the payment."
        )

@router.get("/payment-history/{user_id}", response_model=List[PaymentHistorySchema], status_code=status.HTTP_200_OK)
async def get_payment_history(user_id: str):
    """
    Fetches the payment history of a user by their user ID.
    """
    try:
        logger.info(f"Fetching payment history for user_id: {user_id}")
        history = await fetch_payment_history(user_id)
        if not history:
            logger.warning(f"No payment history found for user_id: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment history not found for the given user ID."
            )
        return history
    except Exception as e:
        logger.error(f"Error while fetching payment history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching payment history."
        )
