from pymongo import MongoClient
from fastapi import HTTPException

# Database setup
client = MongoClient("mongodb://localhost:27017/")
db = client["betting_db"]
bets_collection = db["bets"]
bet_history_collection = db["bet_history"]

# Fetch available bets
async def fetch_bets():
    bets = list(bets_collection.find())
    return bets

# Place a bet
async def place_bet(bet_details: dict):
    result = bets_collection.insert_one(bet_details)
    return {"message": "Bet placed successfully", "bet_id": str(result.inserted_id)}

# Fetch bet history for a user
async def fetch_bet_history(user_id: str):
    bet_history = list(bet_history_collection.find({"user_id": user_id}))
    return bet_history
