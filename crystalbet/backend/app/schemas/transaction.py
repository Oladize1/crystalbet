# schemas/transaction.py
from pydantic import BaseModel,ConfigDict
from typing import Optional

class TransactionCreate(BaseModel):
    amount: float
    status: str  # e.g., 'completed', 'pending', 'failed'

class TransactionResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    status: str
    created_at: str
