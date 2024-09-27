from fastapi import APIRouter, Depends, HTTPException, status
from models.transaction import PaymentRequest
from database import MongoDBConnection  # Use your connection class
from security import get_current_user
import logging

router = APIRouter()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/deposit", status_code=status.HTTP_201_CREATED)
async def deposit_funds(payment_data: PaymentRequest, user: dict = Depends(get_current_user)):
    # Validate the amount
    if payment_data.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be greater than zero")
    
    transaction = {
        "user_id": user["_id"], 
        "amount": payment_data.amount, 
        "method": payment_data.method, 
        "type": "deposit"
    }
    
    try:
        result = await MongoDBConnection.get_database()["transactions"].insert_one(transaction)
        logger.info(f"Deposit successful: {transaction} with transaction ID {result.inserted_id}")
        return {"message": f"Successfully deposited {payment_data.amount} via {payment_data.method}", "transaction_id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Failed to deposit funds: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing deposit")

@router.post("/withdraw", status_code=status.HTTP_201_CREATED)
async def withdraw_funds(payment_data: PaymentRequest, user: dict = Depends(get_current_user)):
    # Validate the amount
    if payment_data.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be greater than zero")
    
    transaction = {
        "user_id": user["_id"], 
        "amount": payment_data.amount, 
        "method": payment_data.method, 
        "type": "withdraw"
    }
    
    try:
        result = await MongoDBConnection.get_database()["transactions"].insert_one(transaction)
        logger.info(f"Withdrawal successful: {transaction} with transaction ID {result.inserted_id}")
        return {"message": f"Successfully withdrew {payment_data.amount} via {payment_data.method}", "transaction_id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Failed to withdraw funds: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing withdrawal")
