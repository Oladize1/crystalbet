from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from db.mongodb import MongoDBConnection
from services.database import fetch_user_profile
from typing import List, Optional, Dict, Any
from services.bet import (
    process_quick_bet,
    process_book_bet,
    fetch_all_bets,
    fetch_live_bets,
    place_bet,
    fetch_bet_history,
    get_filtered_games,
    fetch_bet_slip,
    fetch_bets_by_odds,
    fetch_todays_events,
    fetch_AZMenu,
    fetch_quick_links,
)
from services.auth import get_current_active_user
from services.database import get_db
import logging

router = APIRouter()

# Initialize logger
logger = logging.getLogger("bet_routes")

# Response models
class ResponseModel(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponseModel(BaseModel):
    detail: str

# Bet response schema
class BetResponseSchema(BaseModel):
    bet_id: str
    match_id: str
    bet_amount: float
    bet_type: str
    odds: float
    potential_win: Optional[float] = None

# Quick Bet schema
class QuickBetSchema(BaseModel):
    match_id: str
    bet_amount: float
    bet_type: str
    odds: float

# Book Bet schema
class BookBetSchema(BaseModel):
    booking_code: str
    bet_amount: float

# Bet History schema
class BetHistorySchema(BaseModel):
    bet_id: str
    match_id: str
    bet_amount: float
    bet_type: str
    odds: float
    status: str
    created_at: str

# Routes
@router.get("/", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Welcome to the Betting Platform", "data": {}}

@router.get("/bets", response_model=List[BetResponseSchema], status_code=status.HTTP_200_OK)
async def get_bets(current_user: Dict = Depends(get_current_active_user)):
    """ Fetch all bets. """
    try:
        logger.info("Fetching all bets")
        bets = await fetch_all_bets(current_user["username"])
        return bets
    except Exception as e:
        logger.error(f"Error fetching bets: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching bets.",
        )

@router.post("/bets", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_bet(bet_details: dict, current_user: Dict = Depends(get_current_active_user)):
    """ Create a new bet. """
    try:
        logger.info(f"Placing a new bet with details: {bet_details}")
        result = await place_bet(bet_details, current_user["username"])
        return {"message": "Bet placed successfully", "data": result}
    except Exception as e:
        logger.error(f"Error placing bet: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while placing the bet.",
        )

@router.get("/live-bets", response_model=List[BetResponseSchema], status_code=status.HTTP_200_OK)
async def get_live_bets(current_user: Dict = Depends(get_current_active_user)):
    """ Fetch all live bets. """
    try:
        logger.info("Fetching live bets")
        live_bets = await fetch_live_bets(current_user["username"])
        return live_bets
    except Exception as e:
        logger.error(f"Error fetching live bets: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching live bets.",
        )

@router.get("/profile/{user_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_user_profile(user_id: str, current_user: Dict = Depends(get_current_active_user)):
    """ Fetch user profile by user ID. """
    try:
        logger.info(f"Fetching profile for user: {user_id}")
        if current_user["username"] != user_id and not current_user["is_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this profile.",
            )
        
        user_profile = await fetch_user_profile(user_id)
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found.",
            )
        
        profile_data = {
            "username": user_profile.username,
            "email": user_profile.email,
            "created_at": user_profile.created_at,
            "updated_at": user_profile.updated_at,
            "bet_history": await fetch_bet_history(user_id),
        }
        
        return {"message": "Profile fetched successfully", "data": profile_data}
    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the user profile.",
        )

@router.post("/book-bet", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def book_a_bet(booking_details: BookBetSchema, current_user: Dict = Depends(get_current_active_user)):
    """ Book a bet using a booking code. """
    try:
        logger.info(f"Booking a bet with details: {booking_details}")
        result = await process_book_bet(booking_details, current_user["username"])
        return {"message": "Bet booking successful", "data": result}
    except Exception as e:
        logger.error(f"Error booking the bet: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while booking the bet.",
        )

@router.get("/betslip", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_betslip(current_user: Dict = Depends(get_current_active_user)):
    """ Fetch bet slip. """
    try:
        logger.info("Fetching bet slip")
        bet_slip = await fetch_bet_slip(current_user["username"])
        return {"message": "Bet Slip", "data": bet_slip}
    except Exception as e:
        logger.error(f"Error fetching bet slip: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the bet slip.",
        )

@router.get("/todays-event", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_todays_event(current_user: Dict = Depends(get_current_active_user)):
    """ Fetch today's event details. """
    try:
        logger.info("Fetching today's events")
        events = await fetch_todays_events()
        return {"message": "Today's Event", "data": events}
    except Exception as e:
        logger.error(f"Error fetching today's event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching today's event.",
        )

@router.get("/AZMenu", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_AZMenu(current_user: Dict = Depends(get_current_active_user)):
    """ Fetch AZ Menu details. """
    try:
        logger.info("Fetching AZ Menu details")
        az_menu = await fetch_AZMenu()
        return {"message": "AZ Menu", "data": az_menu}
    except Exception as e:
        logger.error(f"Error fetching AZ Menu: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching AZ Menu.",
        )

@router.get("/quick-links", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_quick_links(current_user: Dict = Depends(get_current_active_user)):
    """ Fetch Quick Links. """
    try:
        logger.info("Fetching Quick Links")
        quick_links = await fetch_quick_links()
        return {"message": "Quick Links", "data": quick_links}
    except Exception as e:
        logger.error(f"Error fetching Quick Links: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching Quick Links.",
        )
