from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from bson import ObjectId
from models.transaction import TransactionSchema, TransactionUpdateSchema
from typing import List, Optional, Dict

# Database setup
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["betting_db"]
transactions_collection = db["transactions"]

# Create a new transaction
async def create_transaction(transaction_data: TransactionSchema) -> Dict[str, str]:
    try:
        transaction_dict = transaction_data.dict()
        result = await transactions_collection.insert_one(transaction_dict)
        return {"message": "Transaction created successfully", "transaction_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")

# Fetch transaction by ID
async def fetch_transaction_by_id(transaction_id: str) -> Dict:
    try:
        transaction = await transactions_collection.find_one({"_id": ObjectId(transaction_id)})
        if transaction:
            return transaction
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transaction: {str(e)}")

# Update transaction by ID
async def update_transaction(transaction_id: str, transaction_update_data: TransactionUpdateSchema) -> Dict[str, str]:
    try:
        update_data = transaction_update_data.dict(exclude_unset=True)
        result = await transactions_collection.update_one({"_id": ObjectId(transaction_id)}, {"$set": update_data})
        
        if result.modified_count == 1:
            return {"message": "Transaction updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Transaction not found or no changes made")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating transaction: {str(e)}")

# Delete a transaction by ID
async def delete_transaction(transaction_id: str) -> Dict[str, str]:
    try:
        result = await transactions_collection.delete_one({"_id": ObjectId(transaction_id)})
        if result.deleted_count == 1:
            return {"message": "Transaction deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting transaction: {str(e)}")

# Fetch transaction history by user ID and status (filtering)
async def fetch_transaction_history(user_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
    try:
        query = {}
        if user_id:
            query["user_id"] = user_id
        if status:
            query["status"] = status
        
        transactions = await transactions_collection.find(query).to_list(length=None)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transaction history: {str(e)}")

# Fetch all transactions (for admin purposes)
async def fetch_all_transactions() -> List[Dict]:
    try:
        transactions = await transactions_collection.find().to_list(length=None)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all transactions: {str(e)}")
