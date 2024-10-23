# app/api/match.py

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from services.match import MatchService
from schemas.match import MatchCreate, MatchUpdate, MatchResponse

router = APIRouter()

@router.post("/", response_model=MatchResponse)
async def create_match(match: MatchCreate):
    match_service = MatchService()
    new_match = await match_service.create_match(match)
    return new_match

@router.get("/", response_model=List[MatchResponse])
async def get_matches():
    match_service = MatchService()
    matches = await match_service.get_all_matches()
    return matches

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: str):
    match_service = MatchService()
    match = await match_service.get_match_by_id(match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(match_id: str, match: MatchUpdate):
    match_service = MatchService()
    updated_match = await match_service.update_match(match_id, match)
    if updated_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return updated_match

@router.delete("/{match_id}")
async def delete_match(match_id: str):
    match_service = MatchService()
    success = await match_service.delete_match(match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"detail": "Match deleted successfully"}
