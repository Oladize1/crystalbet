# models/payment.py

from typing import Any, Dict, Optional
from datetime import datetime

class Payment:
    def __init__(self, user_id: str, amount: float, payment_method: str, 
                 description: Optional[str] = None, transaction_id: Optional[str] = None,
                 payment_status: Optional[str] = None, timestamp: Optional[datetime] = None):
        self.user_id = user_id
        self.amount = amount
        self.payment_method = payment_method
        self.description = description
        self.transaction_id = transaction_id
        self.payment_status = payment_status
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "description": self.description,
            "transaction_id": self.transaction_id,
            "payment_status": self.payment_status,
            "timestamp": self.timestamp.isoformat(),
        }

# You can also define a separate class for payment history if needed
class PaymentHistory:
    def __init__(self, transaction_id: str, amount: float, payment_method: str, 
                 payment_status: str, timestamp: datetime):
        self.transaction_id = transaction_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "timestamp": self.timestamp.isoformat(),
        }
