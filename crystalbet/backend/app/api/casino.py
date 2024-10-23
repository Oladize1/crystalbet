# api/casino.py

from fastapi import APIRouter, HTTPException, Depends
from services.casino import CasinoService
from schemas.casino import CasinoGameCreate, CasinoGameResponse, CasinoGamesResponse
from motor.motor_asyncio import AsyncIOMotorClient
from db.mongodb import init_db,get_collection  # Assuming you have a function to get your MongoDB client

router = APIRouter()

@router.post("/api/casino", response_model=CasinoGameResponse)
async def create_casino_game(game: CasinoGameCreate, db: AsyncIOMotorClient = Depends(get_collection)):
    service = CasinoService(db)
    return await service.create_game(game)

@router.get("/api/casino", response_model=CasinoGamesResponse)
async def get_casino_games(db: AsyncIOMotorClient = Depends(get_collection)):
    service = CasinoService(db)
    games = await service.get_games()
    return CasinoGamesResponse(games=games)

@router.get("/api/casino/{game_id}", response_model=CasinoGameResponse)
async def get_casino_game(game_id: str, db: AsyncIOMotorClient = Depends(get_collection)):
    service = CasinoService(db)
    game = await service.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.put("/api/casino/{game_id}", response_model=CasinoGameResponse)
async def update_casino_game(game_id: str, game: CasinoGameCreate, db: AsyncIOMotorClient = Depends(get_collection)):
    service = CasinoService(db)
    updated_game = await service.update_game(game_id, game)
    if not updated_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return updated_game

@router.delete("/api/casino/{game_id}")
async def delete_casino_game(game_id: str, db: AsyncIOMotorClient = Depends(get_collection)):
    service = CasinoService(db)
    success = await service.delete_game(game_id)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message": "Game deleted successfully"}
