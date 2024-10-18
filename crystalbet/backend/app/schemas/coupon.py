# schemas/coupon.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CouponCreate(BaseModel):
    code: str = Field(..., description="The coupon code")
    discount: float = Field(..., description="The discount amount")
    expiry_date: str = Field(..., description="The expiry date of the coupon in YYYY-MM-DD format")

class CouponOut(BaseModel):
    id: str
    code: str
    discount: float
    expiry_date: str

    class Config:
        from_attributes = True

class CouponCheck(BaseModel):
    code: str = Field(..., description="The coupon code to validate")
