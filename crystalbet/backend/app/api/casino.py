from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from typing import List
from services.casino import CasinoService
from schemas.casino import CasinoGame, CasinoGameCreate, CasinoGameUpdate
from db.mongodb import get_db  # Assuming you have a function to get the DB connection

router = APIRouter()

@router.get("/", response_model=List[CasinoGame])
async def get_casino_games(db=Depends(get_db)):
    """Get a list of casino games."""
    casino_service = CasinoService(db)  # Pass the database connection to the service
    games = await casino_service.get_all_games()
    return games

@router.get("/{game_id}", response_model=CasinoGame)
async def get_casino_game(game_id: str, db=Depends(get_db)):
    """Get details of a specific casino game by ID."""
    casino_service = CasinoService(db)  # Pass the database connection to the service
    game = await casino_service.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post("/", response_model=CasinoGame)
async def create_casino_game(game: CasinoGameCreate, db=Depends(get_db)):
    """Create a new casino game."""
    casino_service = CasinoService(db)  # Pass the database connection to the service
    new_game = await casino_service.create_game(game)
    return new_game

@router.put("/{game_id}", response_model=CasinoGame)
async def update_casino_game(game_id: str, game: CasinoGameUpdate, db=Depends(get_db)):
    """Update an existing casino game by ID."""
    casino_service = CasinoService(db)  # Pass the database connection to the service
    updated_game = await casino_service.update_game(game_id, game)
    if not updated_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return updated_game

@router.delete("/{game_id}")
async def delete_casino_game(game_id: str, db=Depends(get_db)):
    """Delete a casino game by ID."""
    casino_service = CasinoService(db)  # Pass the database connection to the service
    result = await casino_service.delete_game(game_id)
    if not result:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"detail": "Game deleted successfully"}
