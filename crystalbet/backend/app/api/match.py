# app/api/match.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from services.match import MatchService
from motor.motor_asyncio import AsyncIOMotorCollection
from db.mongodb import get_db, get_collection  # Import your database connection function

router = APIRouter()

class MatchResponse(BaseModel):
    id: str = Field(..., alias="_id")
    team_a: str
    team_b: str
    score: str
    status: str
    start_time: str

    class Config:
        allow_population_by_field_name = True

# Dependency function to create MatchService instance
def get_match_service(collection: AsyncIOMotorCollection = Depends(get_collection)):
    return MatchService(collection)

@router.get("/", response_model=List[MatchResponse])
async def get_all_matches(service: MatchService = Depends(get_match_service)):
    matches = await service.get_all_matches()
    return matches

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: str, service: MatchService = Depends(get_match_service)):
    match = await service.get_match(match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.post("/", response_model=MatchResponse)
async def create_match(match: MatchResponse, service: MatchService = Depends(get_match_service)):
    new_match = await service.create_match(match.model_dump())
    return new_match

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(match_id: str, match: MatchResponse, service: MatchService = Depends(get_match_service)):
    updated_match = await service.update_match(match_id, match.model_dump())
    if updated_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return updated_match

@router.delete("/{match_id}", response_model=dict)
async def delete_match(match_id: str, service: MatchService = Depends(get_match_service)):
    deleted = await service.delete_match(match_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"detail": "Match deleted successfully"}
@router.get("/{match_id}/markets", response_model=List[dict])
async def get_match_markets(match_id: str, service: MatchService = Depends(get_match_service)):
    match = await service.get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    # Assuming markets are a field in the match document
    return match.get("markets", [])
