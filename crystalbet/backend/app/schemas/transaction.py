from pydantic import BaseModel
from typing import List, Optional

class TransactionCreateSchema(BaseModel):
    user_id: str
    amount: float
    bet_type: str
    odds: float

class TransactionResponseSchema(BaseModel):
    transaction_id: str
    message: str

class TransactionDetailSchema(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    bet_type: str
    odds: float
    created_at: str
    updated_at: str

class TransactionHistoryResponseSchema(BaseModel):
    user_id: str
    transactions: List[TransactionDetailSchema]
