# services/transactions.py
from pymongo.collection import Collection
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionResponse
from datetime import datetime
from bson import ObjectId

class TransactionService:
    def __init__(self, db):
        self.collection: Collection = db["transactions"]  # Ensure collection name matches your database

    async def create_transaction(self, transaction: TransactionCreate, user_id: str) -> TransactionResponse:
        transaction_data = transaction.dict()
        transaction_data["user_id"] = user_id
        transaction_data["created_at"] = str(datetime.datetime.utcnow())  # Add timestamp

        result = await self.collection.insert_one(transaction_data)
        transaction_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
        return TransactionResponse(**transaction_data)

    async def get_user_transactions(self, user_id: str, skip: int = 0, limit: int = 10) -> list[TransactionResponse]:
        transactions = await self.collection.find({"user_id": user_id}).skip(skip).limit(limit).to_list(length=limit)
        return [TransactionResponse(**transaction) for transaction in transactions]

    async def get_transaction(self, transaction_id: str, user_id: str) -> TransactionResponse:
        transaction = await self.collection.find_one({"_id": ObjectId(transaction_id), "user_id": user_id})
        return TransactionResponse(**transaction) if transaction else None
