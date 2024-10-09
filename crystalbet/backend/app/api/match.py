from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.match import (
    create_match,
    fetch_matches,
    update_match,
    delete_match,
    fetch_live_matches,
    fetch_match_by_id,
    fetch_sports_by_category,
    fetch_live_stream,
    fetch_casino_games,
    fetch_virtual_games,
    check_coupon
)
import logging

router = APIRouter()

# Initialize logger for this module
logger = logging.getLogger("match_routes")

# Response models
class ResponseModel(BaseModel):
    message: str
    data: Dict[str, Any]

class ErrorResponseModel(BaseModel):
    detail: str

# Match schemas
class MatchSchema(BaseModel):
    match_id: Optional[str]
    team_a: str
    team_b: str
    date: str  # Use ISO 8601 format (e.g., "2024-10-01T14:30:00Z")
    venue: str
    status: str  # e.g., "scheduled", "ongoing", "completed"

class UpdateMatchSchema(BaseModel):
    match_id: str
    status: str
    date: Optional[str] = None
    venue: Optional[str] = None

# Routes for match operations

@router.post("/matches", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_match_route(match_details: MatchSchema):
    """
    Creates a new match.
    """
    try:
        logger.info(f"Creating a new match: {match_details}")
        result = await create_match(match_details)
        return {"message": "Match created successfully", "data": result}
    except Exception as e:
        logger.error(f"Error while creating match: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the match."
        )

@router.get("/matches", response_model=List[MatchSchema], status_code=status.HTTP_200_OK)
async def get_matches():
    """
    Fetches all matches.
    """
    try:
        logger.info("Fetching all matches")
        matches = await fetch_matches()
        if not matches:
            logger.warning("No matches found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches found.")
        return matches
    except Exception as e:
        logger.error(f"Error while fetching matches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching matches."
        )

@router.get("/live-bets", response_model=List[MatchSchema], status_code=status.HTTP_200_OK)
async def get_live_matches():
    """
    Fetches all live matches for betting.
    """
    try:
        logger.info("Fetching all live matches")
        live_matches = await fetch_live_matches()
        if not live_matches:
            logger.warning("No live matches found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No live matches found.")
        return live_matches
    except Exception as e:
        logger.error(f"Error while fetching live matches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching live matches."
        )

@router.get("/match/{id}", response_model=MatchSchema, status_code=status.HTTP_200_OK)
async def get_match_by_id(id: str):
    """
    Fetches details of a specific match by its ID.
    """
    try:
        logger.info(f"Fetching match with ID: {id}")
        match = await fetch_match_by_id(id)
        if not match:
            logger.warning(f"No match found with ID: {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found.")
        return match
    except Exception as e:
        logger.error(f"Error while fetching match by ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the match."
        )

@router.get("/sports/{category}", response_model=List[MatchSchema], status_code=status.HTTP_200_OK)
async def get_sports_by_category(category: str):
    """
    Fetches sports matches by category (e.g., football, basketball).
    """
    try:
        logger.info(f"Fetching sports matches for category: {category}")
        matches = await fetch_sports_by_category(category)
        if not matches:
            logger.warning(f"No matches found for category: {category}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches found for this category.")
        return matches
    except Exception as e:
        logger.error(f"Error while fetching matches for category: {category}, error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching matches for this category."
        )

@router.get("/live-stream/{matchId}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_live_stream(matchId: str):
    """
    Fetches the live stream of a specific match.
    """
    try:
        logger.info(f"Fetching live stream for match ID: {matchId}")
        stream_data = await fetch_live_stream(matchId)
        if not stream_data:
            logger.warning(f"No live stream found for match ID: {matchId}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Live stream not found.")
        return {"message": "Live stream fetched successfully", "data": stream_data}
    except Exception as e:
        logger.error(f"Error while fetching live stream for match ID: {matchId}, error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the live stream."
        )

@router.get("/casino", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_casino_games():
    """
    Fetches available casino games.
    """
    try:
        logger.info("Fetching casino games")
        games = await fetch_casino_games()
        if not games:
            logger.warning("No casino games found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No casino games found.")
        return {"message": "Casino games fetched successfully", "data": games}
    except Exception as e:
        logger.error(f"Error while fetching casino games: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching casino games."
        )

@router.get("/virtuals", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_virtual_games():
    """
    Fetches available virtual games.
    """
    try:
        logger.info("Fetching virtual games")
        virtuals = await fetch_virtual_games()
        if not virtuals:
            logger.warning("No virtual games found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No virtual games found.")
        return {"message": "Virtual games fetched successfully", "data": virtuals}
    except Exception as e:
        logger.error(f"Error while fetching virtual games: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching virtual games."
        )

@router.post("/coupon-check", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def check_coupon_code(coupon: str):
    """
    Checks if a coupon code is valid.
    """
    try:
        logger.info(f"Checking coupon code: {coupon}")
        result = await check_coupon(coupon)
        if not result:
            logger.warning(f"Coupon code not found: {coupon}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon code not found.")
        return {"message": "Coupon code is valid", "data": result}
    except Exception as e:
        logger.error(f"Error while checking coupon code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while checking the coupon code."
        )
