# api/bets.py

from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from typing import List
from pymongo.collection import Collection
from models.bet import Bet, BetInDB  # Assuming these models are properly defined
from schemas.bet import BetCreate, BetResponse, BetSlipResponse  # Assuming these schemas are properly defined
from services.database import get_all_bets  # Correct import for the MongoDB collection
from services.auth import get_current_user  # Auth dependency for getting the logged-in user

router = APIRouter(prefix="/bets", tags=["Bets"])

# Helper function to convert MongoDB object to BetResponse
def bet_to_response(bet: BetInDB) -> BetResponse:
    return BetResponse(
        id=str(bet["_id"]),
        user_id=str(bet["user_id"]),
        event=bet["event"],
        odds=bet["odds"],
        amount=bet["amount"],
        potential_win=bet["potential_win"],
        status=bet["status"],
        created_at=bet["created_at"]
    )

@router.get("/", response_model=List[BetResponse])
async def get_all_bets(bets_collection: Collection = Depends(get_all_bets)):
    bets = list(bets_collection.find())
    return [bet_to_response(bet) for bet in bets]

@router.get("/live", response_model=List[BetResponse])
async def get_live_bets(bets_collection: Collection = Depends(get_all_bets)):
    live_bets = list(bets_collection.find({"status": "live"}))
    return [bet_to_response(bet) for bet in live_bets]

@router.post("/book", response_model=BetResponse)
async def book_bet(bet_data: BetCreate, current_user: str = Depends(get_current_user), bets_collection: Collection = Depends(get_all_bets)):
    new_bet = {
        "user_id": ObjectId(current_user),
        "event": bet_data.event,
        "odds": bet_data.odds,
        "amount": bet_data.amount,
        "potential_win": bet_data.odds * bet_data.amount,
        "status": "booked",
        "created_at": bet_data.created_at,
    }
    inserted_bet = bets_collection.insert_one(new_bet)
    return bet_to_response(new_bet)

@router.get("/betslip", response_model=BetSlipResponse)
async def view_bet_slip(current_user: str = Depends(get_current_user), bets_collection: Collection = Depends(get_all_bets)):
    user_bets = list(bets_collection.find({"user_id": ObjectId(current_user)}))
    return BetSlipResponse(bets=[bet_to_response(bet) for bet in user_bets])

@router.get("/odds-less-than/{value}", response_model=List[BetResponse])
async def filter_bets_by_odds(value: float, bets_collection: Collection = Depends(get_all_bets)):
    filtered_bets = list(bets_collection.find({"odds": {"$lt": value}}))
    return [bet_to_response(bet) for bet in filtered_bets]
