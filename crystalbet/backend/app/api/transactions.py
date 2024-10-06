from fastapi import APIRouter, HTTPException
from services.transaction import (
    create_transaction,
    fetch_all_transactions,
    fetch_transaction_by_id,
    update_transaction,
    delete_transaction,
    fetch_transaction_history
)
from models.transaction import TransactionSchema, TransactionUpdateSchema

router = APIRouter()

# Create a new transaction
@router.post("/transactions", response_model=dict)
async def create_new_transaction(transaction: TransactionSchema):
    return await create_transaction(transaction)

# Fetch all transactions
@router.get("/transactions", response_model=list)
async def get_all_transactions():
    return await fetch_all_transactions()

# Fetch transaction by ID
@router.get("/transactions/{transaction_id}", response_model=dict)
async def get_transaction(transaction_id: str):
    return await fetch_transaction_by_id(transaction_id)

# Update a transaction by ID
@router.put("/transactions/{transaction_id}", response_model=dict)
async def update_existing_transaction(transaction_id: str, transaction_update: TransactionUpdateSchema):
    return await update_transaction(transaction_id, transaction_update)

# Delete a transaction by ID
@router.delete("/transactions/{transaction_id}", response_model=dict)
async def delete_existing_transaction(transaction_id: str):
    return await delete_transaction(transaction_id)

# Filter transactions by user ID or status
@router.get("/transactions/filter", response_model=list)
async def filter_transactions_route(user_id: str = None, status: str = None):
    return await fetch_transaction_history(user_id, status)
