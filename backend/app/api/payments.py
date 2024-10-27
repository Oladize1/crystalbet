# app/api/payments.py

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.payment import PaymentCreate, PaymentResponse
from services.payment import PaymentService
from pymongo import MongoClient
from typing import List
router = APIRouter()

# Dependency to get the database
def get_db():
    client = MongoClient("mongodb://localhost:27017")  # Adjust as needed
    return client

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(payment_data: PaymentCreate, db: MongoClient = Depends(get_db)):
    service = PaymentService(db)
    return await service.create_payment(payment_data)

@router.get("/{payment_id}", response_model=PaymentResponse)
async def read_payment(payment_id: str, db: MongoClient = Depends(get_db)):
    service = PaymentService(db)
    return await service.get_payment(payment_id)

@router.get("/", response_model=List[PaymentResponse])
async def list_payments(db: MongoClient = Depends(get_db)):
    service = PaymentService(db)
    return await service.list_payments()
