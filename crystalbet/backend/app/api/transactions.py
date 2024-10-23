# api/transactions.py
from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionResponse
from services.transaction import TransactionService
from core.security import get_current_user

router = APIRouter()

# Dependency
def get_database():
    client = MongoClient("mongodb://localhost:27017")  # Update with your MongoDB URI
    return client["your_database_name"]  # Change this to your database name

@router.post("/api/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db=Depends(get_database), user=Depends(get_current_user)):
    service = TransactionService(db)
    created_transaction = await service.create_transaction(transaction, user.id)
    return created_transaction

@router.get("/api/transactions", response_model=list[TransactionResponse])
async def list_transactions(skip: int = 0, limit: int = 10, db=Depends(get_database), user=Depends(get_current_user)):
    service = TransactionService(db)
    transactions = await service.get_user_transactions(user.id, skip, limit)
    return transactions

@router.get("/api/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str, db=Depends(get_database), user=Depends(get_current_user)):
    service = TransactionService(db)
    transaction = await service.get_transaction(transaction_id, user.id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
