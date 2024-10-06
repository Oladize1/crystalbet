from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.app.services.match import (
    create_match,
    fetch_matches,
    update_match,
    delete_match
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

@router.put("/matches/{match_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def update_match_route(match_id: str, update_details: UpdateMatchSchema):
    """
    Updates an existing match.
    """
    try:
        logger.info(f"Updating match: {match_id} with details: {update_details}")
        result = await update_match(match_id, update_details)
        return {"message": "Match updated successfully", "data": result}
    except Exception as e:
        logger.error(f"Error while updating match: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the match."
        )

@router.delete("/matches/{match_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def delete_match_route(match_id: str):
    """
    Deletes a match by match ID.
    """
    try:
        logger.info(f"Deleting match: {match_id}")
        result = await delete_match(match_id)
        return {"message": "Match deleted successfully", "data": result}
    except Exception as e:
        logger.error(f"Error while deleting match: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the match."
        )
