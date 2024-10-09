#models/transaction.py
from pydantic import BaseModel
from typing import Optional, List

class TransactionSchema(BaseModel):
    user_id: str
    amount: float
    bet_type: str
    odds: float
    created_at: Optional[str] = None  # You may want to use datetime here
    updated_at: Optional[str] = None

class TransactionUpdateSchema(BaseModel):
    transaction_id: str
    amount: Optional[float] = None
    bet_type: Optional[str] = None
    odds: Optional[float] = None
    status: Optional[str] = None  # e.g., 'active', 'settled', 'canceled'

class BetHistorySchema(BaseModel):
    user_id: str
    transactions: List[TransactionSchema]
