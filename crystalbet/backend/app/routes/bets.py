from fastapi import APIRouter, HTTPException, status, Depends, get_db
from pydantic import BaseModel
from typing import List, Optional
from schemas.bet import QuickBetSchema, BookBetSchema, BetHistorySchema
from app.services.bet import (
    fetch_bets,
    place_bet,
    fetch_bet_history,
    process_quick_bet,
    GameSlot , process_book_bet
)

router = APIRouter()

# Response models
class ResponseModel(BaseModel):
    message: str
    data: dict

class ErrorResponseModel(BaseModel):
    detail: str

# Define BetResponseSchema if necessary
class BetResponseSchema(BaseModel):
    bet_id: str
    match_id: str
    bet_amount: float
    bet_type: str
    odds: float
    potential_win: Optional[float] = None

# GameSlot schema
class GameSlotSchema(BaseModel):
    name: str
    category: str
    provider: str
    description: str
    image_url: str

class GameSlot:
    def __init__(self, db):
        self.collection = db["game_slots"]

    def find_games(self, category: str, provider: Optional[str]):
        query = {}
        if category != 'All':
            query["category"] = category
        if provider:
            query["provider"] = provider

        return list(self.collection.find(query))

# Dependency to get the game slot model
def get_game_slot_model(db=Depends(get_db)):
    return GameSlot(db)

@router.get("/bets", response_model=List[BetResponseSchema], status_code=status.HTTP_200_OK)
async def get_bets():
    """ Fetches all bets. """
    try:
        bets = await fetch_bets()
        return bets
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching bets."
        )

@router.post("/bets", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_bet(bet_details: dict):
    """ Creates a new bet. """
    try:
        result = await place_bet(bet_details)
        return {"message": "Bet placed successfully", "data": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while placing the bet."
        )

@router.get("/bet-history/{user_id}", response_model=List[BetHistorySchema], status_code=status.HTTP_200_OK)
async def get_bet_history(user_id: str):
    """ Fetches the betting history of a user by their user ID. """
    try:
        history = await fetch_bet_history(user_id)
        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bet history not found for the given user ID."
            )
        return history
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching bet history."
        )

@router.post("/quick-bet", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def quick_bet(bet_details: QuickBetSchema):
    """ Processes a quick bet based on user input. """
    try:
        result = await process_quick_bet(bet_details)
        return {"message": "Quick bet placed successfully", "data": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the quick bet."
        )

@router.post("/book-bet", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def book_a_bet(booking_details: BookBetSchema):
    """ Books a bet using a booking code. """
    try:
        result = await process_book_bet(booking_details)
        return {"message": "Bet booking successful", "data": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while booking the bet."
        )

@router.get("/game-slots", response_model=List[GameSlotSchema], status_code=status.HTTP_200_OK)
async def get_game_slots(category: str = 'All', provider: Optional[str] = None, game_slot_model: GameSlot = Depends(get_game_slot_model)):
    """ Fetches game slots based on category and provider. """
    try:
        games = game_slot_model.find_games(category, provider)
        if not games:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No game slots found."
            )
        return games
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching game slots."
        )
