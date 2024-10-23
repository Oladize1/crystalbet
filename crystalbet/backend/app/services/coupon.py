# services/coupon.py
from typing import Optional
from models.coupon import Coupon
from schemas.coupon import CouponCreate, CouponCheck
from mongoengine import DoesNotExist
from datetime import datetime

class CouponService:
    @staticmethod
    def create_coupon(coupon_data: CouponCreate) -> Coupon:
        coupon = Coupon(
            code=coupon_data.code,
            discount=coupon_data.discount,
            expiry_date=datetime.strptime(coupon_data.expiry_date, "%Y-%m-%d")
        )
        coupon.save()
        return coupon

    @staticmethod
    def validate_coupon(coupon_data: CouponCheck) -> Optional[Coupon]:
        try:
            coupon = Coupon.objects.get(code=coupon_data.code)
            if coupon.is_expired():
                return None
            return coupon
        except DoesNotExist:
            return None
