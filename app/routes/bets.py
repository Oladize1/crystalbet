from fastapi import APIRouter
from services.bets import fetch_bets, place_bet, fetch_bet_history

router = APIRouter()

@router.get("/bets")
async def get_bets():
    return await fetch_bets()

@router.post("/bets")
async def create_bet(bet_details: dict):
    return await place_bet(bet_details)

@router.get("/bet-history/{user_id}")
async def get_bet_history(user_id: str):
    return await fetch_bet_history(user_id)
