# api/match.py
from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from services.match import MatchService
from schemas.match import MatchCreate, MatchResponse, MatchListResponse

router = APIRouter()

# Dependency to get MongoDB client
def get_db() -> MongoClient:
    client = MongoClient("mongodb://localhost:27017")  # Change the connection string as needed
    return client["your_database_name"]  # Change to your database name

@router.post("/matches", response_model=MatchResponse)
async def create_match(match_create: MatchCreate, db: MongoClient = Depends(get_db)):
    service = MatchService(db)
    return await service.create_match(match_create)

@router.get("/matches/{match_id}", response_model=MatchResponse)
async def get_match(match_id: str, db: MongoClient = Depends(get_db)):
    service = MatchService(db)
    match = await service.get_match(match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.get("/matches", response_model=MatchListResponse)
async def get_all_matches(db: MongoClient = Depends(get_db)):
    service = MatchService(db)
    matches = await service.get_all_matches()
    return MatchListResponse(matches=matches)

@router.put("/matches/{match_id}", response_model=MatchResponse)
async def update_match(match_id: str, match_update: MatchCreate, db: MongoClient = Depends(get_db)):
    service = MatchService(db)
    return await service.update_match(match_id, match_update)

@router.delete("/matches/{match_id}")
async def delete_match(match_id: str, db: MongoClient = Depends(get_db)):
    service = MatchService(db)
    await service.delete_match(match_id)
    return {"detail": "Match deleted"}
