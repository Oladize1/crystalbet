from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.payment import (
    initiate_payment,
    confirm_payment,
    fetch_payment_history,
)
# Payment Schemas
from schemas.payment import (
    InitiatePaymentSchema,
    ConfirmPaymentSchema,
    PaymentHistorySchema,
    PaymentResponseModel,
    ErrorResponseModel
)

from models.payment import Payment, PaymentHistory
from services.bet import (
    fetch_all_bets,
    fetch_live_bets,
    process_book_bet,
    fetch_bet_slip,
    fetch_sports_category,
    fetch_live_stream,
    get_match,
    get_casino,
    get_virtuals,
    coupon_check,
    get_todays_event,
    cms_access,
    odds_less_than,
)
import logging

router = APIRouter()

# Initialize logger
logger = logging.getLogger("bet_payment_routes")

# Response models
class PaymentResponseModel(BaseModel):
    message: str
    data: Dict[str, Any]

class ErrorResponseModel(BaseModel):
    detail: str

# Define payment schemas
class InitiatePaymentSchema(BaseModel):
    user_id: str
    amount: float
    payment_method: str
    description: Optional[str] = None

class ConfirmPaymentSchema(BaseModel):
    user_id: str
    transaction_id: str
    payment_status: str

class PaymentHistorySchema(BaseModel):
    transaction_id: str
    amount: float
    payment_method: str
    payment_status: str
    timestamp: str

# Routes for payment and bet operations

# Home endpoint
@router.get("/", response_model=Dict[str, Any])
async def home():
    logger.info("Accessing home")
    return {"message": "Welcome to the Home Page"}

# Bets endpoint
@router.get("/bets", response_model=List[Dict[str, Any]])
async def get_bets():
    logger.info("Fetching all bets")
    return await fetch_all_bets()

# Live Bets endpoint
@router.get("/live-bets", response_model=List[Dict[str, Any]])
async def live_bets():
    logger.info("Fetching live bets")
    return await fetch_live_bets()

# User Profile endpoint
@router.get("/profile", response_model=Dict[str, Any])
async def user_profile():
    logger.info("Accessing user profile")
    # Mock profile, actual implementation may require user authentication
    return {"user": "John Doe", "email": "johndoe@example.com"}

# Book Bet endpoint
@router.post("/book-bet", response_model=Dict[str, Any])
async def book_bet_route(bet_details: Dict[str, Any]):
    logger.info(f"Booking bet: {bet_details}")
    return await process_book_bet(bet_details)

# Bet Slip endpoint
@router.get("/betslip", response_model=Dict[str, Any])
async def betslip():
    logger.info("Fetching bet slip")
    return await fetch_bet_slip()

# Sports Category endpoint
@router.get("/sports/{category}", response_model=List[Dict[str, Any]])
async def sports_category(category: str):
    logger.info(f"Fetching sports category: {category}")
    return await fetch_sports_category(category)

# Live Stream endpoint
@router.get("/live-stream/{matchId}", response_model=Dict[str, Any])
async def live_stream(matchId: str):
    logger.info(f"Fetching live stream for match: {matchId}")
    return await fetch_live_stream(matchId)

# Match Details endpoint
@router.get("/match/{id}", response_model=Dict[str, Any])
async def match_details(id: str):
    logger.info(f"Fetching match details for ID: {id}")
    return await get_match(id)

# Casino endpoint
@router.get("/casino", response_model=Dict[str, Any])
async def casino():
    logger.info("Accessing casino")
    return await get_casino()

# Virtuals endpoint
@router.get("/virtuals", response_model=Dict[str, Any])
async def virtuals():
    logger.info("Fetching virtuals")
    return await get_virtuals()

# Coupon Check endpoint
@router.get("/coupon-check", response_model=Dict[str, Any])
async def coupon_check_route():
    logger.info("Checking coupon")
    return await coupon_check()

# CMS endpoint
@router.get("/cms", response_model=Dict[str, Any])
async def cms_route():
    logger.info("Accessing CMS")
    return await cms_access()

# Odds Less Than endpoint
@router.get("/odds-less-than", response_model=Dict[str, Any])
async def odds_less_than_route():
    logger.info("Fetching odds less than certain value")
    return await odds_less_than()

# Today's Event endpoint
@router.get("/todays-event", response_model=List[Dict[str, Any]])
async def todays_event():
    logger.info("Fetching today's event")
    return await get_todays_event()

# Initiate Payment endpoint
@router.post("/initiate-payment", response_model=PaymentResponseModel, status_code=status.HTTP_201_CREATED)
async def initiate_payment_route(payment_details: InitiatePaymentSchema):
    logger.info(f"Initiating payment: {payment_details}")
    result = await initiate_payment(payment_details.dict())
    return {"message": "Payment initiated successfully", "data": result}

# Confirm Payment endpoint
@router.post("/confirm-payment", response_model=PaymentResponseModel, status_code=status.HTTP_200_OK)
async def confirm_payment_route(payment_details: ConfirmPaymentSchema):
    logger.info(f"Confirming payment: {payment_details}")
    result = await confirm_payment(payment_details.transaction_id)
    return {"message": "Payment confirmed successfully", "data": result}

# Payment History endpoint
@router.get("/payment-history/{user_id}", response_model=List[PaymentHistorySchema], status_code=status.HTTP_200_OK)
async def get_payment_history(user_id: str):
    logger.info(f"Fetching payment history for user_id: {user_id}")
    history = await fetch_payment_history(user_id)
    if not history:
        logger.warning(f"No payment history found for user_id: {user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment history not found")
    return history
