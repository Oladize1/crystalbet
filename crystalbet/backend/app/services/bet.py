from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from models.bet import QuickBetSchema, BookBetSchema, GameSlot
from bson import ObjectId

# Database setup
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["betting_db"]
bets_collection = db["bets"]
bet_history_collection = db["bet_history"]

# Helper function to calculate potential win
def calculate_potential_win(bet_amount: float, odds: float) -> float:
    """Calculate potential win based on bet amount and odds."""
    return bet_amount * odds

# Process a quick bet
async def process_quick_bet(bet_details: QuickBetSchema):
    """Process a quick bet and calculate potential win if not provided."""
    try:
        bet_data = bet_details.dict()

        # Calculate potential win if it's not provided
        if "potential_win" not in bet_data:
            total_odds = 1.0
            for selection in bet_data["selections"]:
                total_odds *= selection["odds"]
            bet_data["odds"] = total_odds
            bet_data["potential_win"] = calculate_potential_win(bet_data["bet_amount"], total_odds)

        result = await bets_collection.insert_one(bet_data)
        return {"message": "Quick bet processed successfully", "bet_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing quick bet: {str(e)}")

# Book a bet using booking code
async def process_book_bet(booking_data: BookBetSchema):
    """Process a bet using booking code."""
    try:
        booking_data_dict = booking_data.dict()
        result = await bets_collection.insert_one(booking_data_dict)
        return {"message": "Bet booked successfully", "booking_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing book bet: {str(e)}")

# Fetch available bets
async def fetch_bets():
    """Fetch and return all available bets."""
    try:
        bets = await bets_collection.find().to_list(length=None)  # Adjust length for pagination
        return bets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bets: {str(e)}")

# Place a regular bet
async def place_bet(bet_details: QuickBetSchema):
    """Place a regular bet and calculate potential win if not provided."""
    try:
        bet_data = bet_details.dict()
        if bet_data.get("potential_win") is None:
            bet_data["potential_win"] = calculate_potential_win(bet_data["bet_amount"], bet_data["odds"])
        
        result = await bets_collection.insert_one(bet_data)
        return {"message": "Bet placed successfully", "bet_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error placing bet: {str(e)}")

# Fetch bet history for a user
async def fetch_bet_history(user_id: str):
    """Fetch the betting history for a specific user."""
    try:
        bet_history = await bet_history_collection.find({"user_id": user_id}).to_list(length=None)  # Adjust length for pagination
        return bet_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bet history: {str(e)}")

# Fetch games based on category and provider
async def get_filtered_games(category: str, provider: str):
    """Fetch and return games based on category and provider."""
    try:
        games = await GameSlot.find_games(category, provider)  # Assuming this is an async function
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching filtered games: {str(e)}")
