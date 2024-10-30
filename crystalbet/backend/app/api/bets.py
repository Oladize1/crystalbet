# api/match.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.match import Match, LiveMatch
from schemas.match import MatchResponse, MatchDetailResponse, LiveMatchResponse, SportCategoryResponse
from services.match import MatchService
from utils.jwt import get_current_user

router = APIRouter(
    prefix="/api/matches",
    tags=["Matches"]
)

# Dependency for MatchService
def get_match_service():
    return MatchService()

@router.get("/", response_model=List[MatchResponse])
async def get_all_matches(match_service: MatchService = Depends(get_match_service)):
    """
    Retrieve all available matches.
    """
    matches = await match_service.get_all_matches()
    if not matches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches found")
    return matches

@router.get("/live", response_model=List[LiveMatchResponse])
async def get_live_matches(match_service: MatchService = Depends(get_match_service)):
    """
    Retrieve all live matches.
    """
    live_matches = await match_service.get_live_matches()
    if not live_matches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No live matches found")
    return live_matches

@router.get("/{match_id}", response_model=MatchDetailResponse)
async def get_match_by_id(match_id: str, match_service: MatchService = Depends(get_match_service)):
    """
    Retrieve match details by match ID.
    """
    match = await match_service.get_match_by_id(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return match

@router.get("/sports/{category}", response_model=List[SportCategoryResponse])
async def get_matches_by_sport_category(category: str, match_service: MatchService = Depends(get_match_service)):
    """
    Retrieve matches by sports category.
    """
    matches = await match_service.get_matches_by_category(category)
    if not matches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches found for this category")
    return matches

@router.get("/today", response_model=List[MatchResponse])
async def get_todays_matches(match_service: MatchService = Depends(get_match_service)):
    """
    Retrieve today's matches.
    """
    todays_matches = await match_service.get_todays_matches()
    if not todays_matches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches available for today")
    return todays_matches
