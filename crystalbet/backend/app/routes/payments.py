from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any
from schemas.bet import QuickBetSchema, BookBetSchema, BetResponseSchema, BetHistorySchema
from backend.app.services.bet import (
    fetch_bets,
    place_bet,
    fetch_bet_history,
    process_quick_bet,
    process_book_bet
)
import logging

router = APIRouter()

# Initialize logger for this module
logger = logging.getLogger("bets_routes")

# Response models
class ResponseModel(BaseModel):
    message: str
    data: Dict[str, Any]

class ErrorResponseModel(BaseModel):
    detail: str

@router.get("/bets", response_model=List[BetResponseSchema], status_code=status.HTTP_200_OK)
async def get_bets():
    """
    Fetches all bets.
    """
    try:
        logger.info("Fetching all bets")
        bets = await fetch_bets()
        if not bets:
            logger.warning("No bets found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bets found.")
        return bets
    except Exception as e:
        logger.error(f"Error while fetching bets: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching bets."
        )

@router.post("/bets", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_bet(bet_details: dict):
    """
    Creates a new bet.
    """
    try:
        logger.info(f"Placing a new bet: {bet_details}")
        result = await place_bet(bet_details)
        return {"message": "Bet placed successfully", "data": result}
    except Exception as e:
        logger.error(f"Error while placing bet: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while placing the bet."
        )

@router.get("/bet-history/{user_id}", response_model=List[BetHistorySchema], status_code=status.HTTP_200_OK)
async def get_bet_history(user_id: str):
    """
    Fetches the betting history of a user by their user ID.
    """
    try:
        logger.info(f"Fetching bet history for user_id: {user_id}")
        history = await fetch_bet_history(user_id)
        if not history:
            logger.warning(f"No bet history found for user_id: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bet history not found for the given user ID."
            )
        return history
    except Exception as e:
        logger.error(f"Error while fetching bet history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching bet history."
        )

@router.post("/quick-bet", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def quick_bet(bet_details: QuickBetSchema):
    """
    Processes a quick bet based on user input.
    """
    try:
        logger.info(f"Processing quick bet: {bet_details}")
        result = await process_quick_bet(bet_details)
        return {"message": "Quick bet placed successfully", "data": result}
    except Exception as e:
        logger.error(f"Error while processing quick bet: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the quick bet."
        )

@router.post("/book-bet", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def book_a_bet(booking_details: BookBetSchema):
    """
    Books a bet using a booking code.
    """
    try:
        logger.info(f"Booking a bet: {booking_details}")
        result = await process_book_bet(booking_details)
        return {"message": "Bet booking successful", "data": result}
    except Exception as e:
        logger.error(f"Error while booking bet: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while booking the bet."
        )
