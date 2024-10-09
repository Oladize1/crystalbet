from fastapi import APIRouter, HTTPException, status, Depends
from services.database import MongoDBConnection
from typing import List, Optional
from utils.jwt import create_access_token  # JWT generation for login
from utils.calculate_odds import calculate_bet_odds  # Odds calculation utility
from core.config import settings
from schemas.bet import (
    BetType,
    BetResult,
    BetDetailSchema,
    QuickBetSchema,
    BookBetSchema,
    BetHistorySchema,
    BetResponseSchema,
    ErrorResponseSchema
)
from bson import ObjectId
import logging
from models.bet import (
    BetType,
    BetStatus,
    LiveBet,
    BetSelection,
    Bet,
    User,
    GameSlot,
    GameSlotResponse,
    QuickBetSchema,
    BookBetSchema,
    LiveBetSchema,
    Casino,
    Virtuals,
    BetHistory,
    CouponCheck,
    Event,
    EventResponse
)


router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ------------------ Home Endpoint ------------------
@router.get("/")
async def read_home():
    """Home page endpoint."""
    logger.info("Home page accessed")
    return {"message": "Welcome to the Home Page"}

# ------------------ Bets Endpoints ------------------
@router.get("/bets", response_model=List[Bet])
async def get_bets():
    """Retrieve all bets from the database."""
    try:
        db = MongoDBConnection.get_database()
        bets = await db["bets"].find().to_list(length=100)
        if not bets:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bets found")
        return bets
    except Exception as e:
        logger.error(f"Error fetching bets: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch bets")

@router.post("/bets", response_model=Bet)
async def create_bet(bet: Bet):
    """Create a new bet in the database."""
    try:
        db = MongoDBConnection.get_database()
        result = await db["bets"].insert_one(bet.dict())
        created_bet = {**bet.dict(), "id": str(result.inserted_id)}
        logger.info(f"Bet created with ID: {created_bet['id']}")
        return created_bet
    except Exception as e:
        logger.error(f"Error creating bet: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create bet")


# ------------------ Live Bets Endpoints ------------------
@router.get("/live-bets", response_model=List[LiveBet])
async def get_live_bets():
    """Retrieve all live bets."""
    try:
        db = MongoDBConnection.get_database()
        live_bets = await db["live_bets"].find().to_list(length=100)
        if not live_bets:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No live bets found")
        return live_bets
    except Exception as e:
        logger.error(f"Error fetching live bets: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch live bets")


# ------------------ User Profile Endpoints ------------------
@router.get("/profile/{user_id}", response_model=User)
async def get_user_profile(user_id: str):
    """Fetch user profile details."""
    try:
        db = MongoDBConnection.get_database()
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch user profile")


# ------------------ Login/Register Endpoints ------------------
@router.post("/login")
async def login_user(email: str, password: str):
    """User login."""
    try:
        db = MongoDBConnection.get_database()
        user = await db["users"].find_one({"email": email, "password": password})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return {"message": "Login successful", "user": user}
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")

@router.post("/register", response_model=User)
async def register_user(user: User):
    """User registration."""
    try:
        db = MongoDBConnection.get_database()
        existing_user = await db["users"].find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        result = await db["users"].insert_one(user.dict())
        new_user = {**user.dict(), "id": str(result.inserted_id)}
        return new_user
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")


# ------------------ Casino & Virtuals Endpoints ------------------
@router.get("/casino", response_model=List[Casino])
async def get_casino_games():
    """Fetch all casino games."""
    try:
        db = MongoDBConnection.get_database()
        games = await db["casino"].find().to_list(length=100)
        if not games:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No casino games found")
        return games
    except Exception as e:
        logger.error(f"Error fetching casino games: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch casino games")

@router.get("/virtuals", response_model=List[Virtuals])
async def get_virtual_games():
    """Fetch all virtual games."""
    try:
        db = MongoDBConnection.get_database()
        games = await db["virtuals"].find().to_list(length=100)
        if not games:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No virtual games found")
        return games
    except Exception as e:
        logger.error(f"Error fetching virtual games: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch virtual games")


# ------------------ Coupon Check Endpoints ------------------
@router.post("/coupon-check")
async def check_coupon(coupon_code: str):
    """Check if a coupon code is valid."""
    try:
        db = MongoDBConnection.get_database()
        coupon = await db["coupons"].find_one({"code": coupon_code})
        if not coupon:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid coupon code")
        return {"message": "Coupon is valid", "coupon": coupon}
    except Exception as e:
        logger.error(f"Error checking coupon: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Coupon check failed")


# ------------------ Today's Event Endpoint ------------------
@router.get("/todays-event", response_model=List[Event])
async def get_todays_event():
    """Fetch today's event details."""
    try:
        db = MongoDBConnection.get_database()
        events = await db["events"].find({"date": {"$eq": "today"}}).to_list(length=100)
        if not events:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No events found for today")
        return events
    except Exception as e:
        logger.error(f"Error fetching today's events: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch today's events")


# ------------------ Sports by Category Endpoints ------------------
@router.get("/sports/{category}")
async def get_sports_by_category(category: str):
    """Fetch sports by category."""
    try:
        db = MongoDBConnection.get_database()
        sports = await db["sports"].find({"category": category}).to_list(length=100)
        if not sports:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No sports found for category {category}")
        return sports
    except Exception as e:
        logger.error(f"Error fetching sports for category {category}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch sports")

# ------------------ Odds Less Than Endpoint ------------------
@router.get("/odds-less-than")
async def get_odds_less_than(odds: float):
    """Fetch all bets with odds less than a specified value."""
    try:
        db = MongoDBConnection.get_database()
        bets = await db["bets"].find({"odds": {"$lt": odds}}).to_list(length=100)
        if not bets:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No bets found with odds less than {odds}")
        return bets
    except Exception as e:
        logger.error(f"Error fetching bets with odds less than {odds}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch bets")
