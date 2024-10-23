# app/services/payment.py

from pymongo import MongoClient
from bson import ObjectId
from typing import List
from models.payment import Payment
from schemas.payment import PaymentCreate, PaymentResponse
from fastapi import HTTPException, status

class PaymentService:
    def __init__(self, db: MongoClient):
        self.collection = db.payments

    async def create_payment(self, payment_data: PaymentCreate) -> PaymentResponse:
        payment = Payment(**payment_data.dict())
        result = await self.collection.insert_one(payment.dict())
        payment.id = result.inserted_id
        return PaymentResponse(**payment.dict())

    async def get_payment(self, payment_id: str) -> PaymentResponse:
        payment = await self.collection.find_one({"_id": ObjectId(payment_id)})
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        return PaymentResponse(**payment)

    async def list_payments(self) -> List[PaymentResponse]:
        payments = await self.collection.find().to_list(length=100)
        return [PaymentResponse(**payment) for payment in payments]
