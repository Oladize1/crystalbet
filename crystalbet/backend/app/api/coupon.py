# api/coupon.py
from fastapi import APIRouter, HTTPException
from schemas.coupon import CouponCreate, CouponOut, CouponCheck
from services.coupon import CouponService

router = APIRouter()

@router.post("/coupons/create", response_model=CouponOut)
async def create_coupon(coupon_data: CouponCreate):
    coupon = CouponService.create_coupon(coupon_data)
    return CouponOut(id=str(coupon.id), code=coupon.code, discount=coupon.discount, expiry_date=coupon.expiry_date.strftime("%Y-%m-%d"))

@router.post("/coupons/check", response_model=CouponOut)
async def check_coupon(coupon_data: CouponCheck):
    coupon = CouponService.validate_coupon(coupon_data)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found or expired")
    return CouponOut(id=str(coupon.id), code=coupon.code, discount=coupon.discount, expiry_date=coupon.expiry_date.strftime("%Y-%m-%d"))
