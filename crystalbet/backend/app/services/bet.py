from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from models.bet import QuickBetSchema, BookBetSchema, GameSlot
from bson import ObjectId
from datetime import datetime
from services.database import fetch_sports_categories
from typing import Optional, Dict, List

# Database setup (Consider moving connection to a separate config file for better separation of concerns)
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["betting_db"]
bets_collection = db["bets"]
bet_history_collection = db["bet_history"]
games_collection = db["games"]
live_stream_collection = db["live_streams"]

# Helper function to calculate potential win
def calculate_potential_win(bet_amount: float, odds: float) -> float:
    """Calculate potential win based on bet amount and odds."""
    return round(bet_amount * odds, 2)

# Process a quick bet
async def process_quick_bet(bet_details: QuickBetSchema, user_id: str):
    """Process a quick bet and calculate potential win if not provided."""
    try:
        bet_data = bet_details.dict()
        bet_data["user_id"] = ObjectId(user_id)
        
        # Calculate potential win if it's not provided
        if "potential_win" not in bet_data or bet_data["potential_win"] is None:
            total_odds = 1.0
            for selection in bet_data["selections"]:
                total_odds *= selection["odds"]
            bet_data["odds"] = total_odds
            bet_data["potential_win"] = calculate_potential_win(bet_data["bet_amount"], total_odds)
        
        result = await bets_collection.insert_one(bet_data)
        await bet_history_collection.insert_one({
            "bet_id": str(result.inserted_id),
            "user_id": ObjectId(user_id),
            "bet_details": bet_data,
            "created_at": datetime.now()
        })
        
        return {"message": "Quick bet processed successfully", "bet_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing quick bet: {str(e)}")

# Book a bet using a booking code
async def process_book_bet(booking_data: BookBetSchema, user_id: str):
    """Process a bet using a booking code."""
    try:
        booking_data_dict = booking_data.dict()
        booking_data_dict["user_id"] = ObjectId(user_id)
        
        # Ensure booking code is valid
        if not booking_data_dict.get("booking_code"):
            raise HTTPException(status_code=400, detail="Booking code is required")
        
        result = await bets_collection.insert_one(booking_data_dict)
        await bet_history_collection.insert_one({
            "bet_id": str(result.inserted_id),
            "user_id": ObjectId(user_id),
            "bet_details": booking_data_dict,
            "created_at": datetime.now()
        })
        
        return {"message": "Bet booked successfully", "booking_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing book bet: {str(e)}")
# Fetch AZ Menu details
async def fetch_AZMenu():
    """Fetch AZ Menu details."""
    try:
        az_menu = await games_collection.find().distinct("name")
        return az_menu
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching AZ Menu: {str(e)}")

# Fetch Quick Links
async def fetch_quick_links():
    """Fetch Quick Links."""
    try:
        quick_links = await games_collection.find().distinct("category")
        return quick_links
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Quick Links: {str(e)}")
# Fetch Quick Links
async def fetch_quick_links():
    """Fetch Quick Links."""
    try:
        quick_links = await games_collection.find().distinct("category")
        return quick_links
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Quick Links: {str(e)}")


# Fetch all bets
async def fetch_all_bets(skip: int = 0, limit: int = 10):
    """Fetch and return all available bets with pagination."""
    try:
        bets = await bets_collection.find().skip(skip).limit(limit).to_list(length=None)
        return bets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bets: {str(e)}")

# Fetch live bets
async def fetch_live_bets():
    """Fetch and return all live bets."""
    try:
        live_bets = await bets_collection.find({"status": "live"}).to_list(length=None)
        return live_bets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching live bets: {str(e)}")

# Fetch bet slip for a user
async def fetch_bet_slip(user_id: str):
    """Fetch the current user's bet slip."""
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID")
        bet_slip = await bets_collection.find({"user_id": ObjectId(user_id), "status": "pending"}).to_list(length=None)
        return bet_slip
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bet slip: {str(e)}")

# Fetch a specific sports category
async def fetch_sports_category(category_id: str) -> Optional[Dict]:
    """Fetch a specific sports category."""
    try:
        categories = await fetch_sports_categories()
        category = next((cat for cat in categories if str(cat["_id"]) == category_id), None)
        return category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sports category: {str(e)}")

# Fetch live stream events
async def fetch_live_stream():
    """Fetch and return live stream events."""
    try:
        live_streams = await live_stream_collection.find({"status": "live"}).to_list(length=None)
        return live_streams
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching live streams: {str(e)}")

# Fetch a specific match
async def get_match(match_id: str) -> Optional[Dict]:
    """Fetch a specific match by ID."""
    try:
        match = await games_collection.find_one({"_id": ObjectId(match_id)})
        return match
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching match: {str(e)}")
    
# Place a regular bet
async def place_bet(bet_details: QuickBetSchema, user_id: str):
    """Place a regular bet and calculate potential win if not provided."""
    try:
        # Validate user ID
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID")

        bet_data = bet_details.dict()
        bet_data["user_id"] = ObjectId(user_id)

        # Calculate potential win if not provided
        if "potential_win" not in bet_data or bet_data["potential_win"] is None:
            if "bet_amount" not in bet_data or "odds" not in bet_data:
                raise HTTPException(status_code=400, detail="Bet amount and odds are required")
            bet_data["potential_win"] = calculate_potential_win(bet_data["bet_amount"], bet_data["odds"])

        # Insert bet data into bets collection
        result = await bets_collection.insert_one(bet_data)

        # Insert bet history
        await bet_history_collection.insert_one({
            "bet_id": str(result.inserted_id),
            "user_id": ObjectId(user_id),
            "bet_details": bet_data,
            "created_at": datetime.now()
        })

        return {"message": "Bet placed successfully", "bet_id": str(result.inserted_id)}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error placing bet: {str(e)}")

# Fetch a specific sports category
async def fetch_sports_category(category_id: str) -> Optional[Dict]:
    """Fetch a specific sports category."""
    try:
        categories = await fetch_sports_categories()
        category = next((cat for cat in categories if str(cat["_id"]) == category_id), None)
        return category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sports category: {str(e)}")
async def get_filtered_games(category: str, provider: str):
    """Fetch and return games based on category and provider."""
    try:
        if not category or not provider:
            raise HTTPException(status_code=400, detail="Category and provider are required")
        games = await games_collection.find({"category": category, "provider": provider}).to_list(length=None)
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching filtered games: {str(e)}")
# Fetch bets with odds less than a given number
async def fetch_bets_by_odds(odds: float):
    """Fetch bets with odds less than the given value."""
    try:
        if odds <= 0:
            raise HTTPException(status_code=400, detail="Odds value must be greater than 0")
        bets = await bets_collection.find({"odds": {"$lt": odds}}).to_list(length=None)
        return bets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bets by odds: {str(e)}")
# Fetch today's events
async def fetch_todays_events():
    """Fetch events happening today."""
    try:
        today = datetime.now().date()
        events = await bets_collection.find({"date": today}).to_list(length=None)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching today's events: {str(e)}")

# Fetch bet history for a user
async def fetch_bet_history(user_id: str):
    """Fetch the betting history for a specific user."""
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID")
        bet_history = await bet_history_collection.find({"user_id": ObjectId(user_id)}).to_list(length=None)
        return bet_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bet history: {str(e)}")


# Fetch casino games
async def get_casino(provider: str):
    """Fetch and return casino games based on the provider."""
    try:
        if not provider:
            raise HTTPException(status_code=400, detail="Provider is required")
        games = await games_collection.find({"provider": provider, "category": "casino"}).to_list(length=None)
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching casino games: {str(e)}")

# Fetch virtual sports
async def get_virtuals(provider: str):
    """Fetch and return virtual sports games."""
    try:
        if not provider:
            raise HTTPException(status_code=400, detail="Provider is required")
        games = await games_collection.find({"provider": provider, "category": "virtual"}).to_list(length=None)
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching virtual sports: {str(e)}")

# Check if coupon code is valid
async def coupon_check(coupon_code: str):
    """Check if a coupon code is valid."""
    try:
        coupon = await bets_collection.find_one({"coupon_code": coupon_code})
        if not coupon:
            raise HTTPException(status_code=404, detail="Coupon code not found")
        return coupon
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking coupon: {str(e)}")

# Fetch today's events
async def get_todays_event():
    """Fetch events happening today."""
    try:
        today = datetime.now().date()
        events = await bets_collection.find({"date": today}).to_list(length=None)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching today's events: {str(e)}")

# Fetch CMS access (Content Management System)
async def cms_access():
    """Fetch CMS access details."""
    try:
        cms_details = await db["cms_access"].find().to_list(length=None)
        return cms_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CMS access: {str(e)}")

# Fetch bets with odds less than a given number
async def odds_less_than(odds: float):
    """Fetch bets with odds less than the given value."""
    try:
        if odds <= 0:
            raise HTTPException(status_code=400, detail="Odds value must be greater than 0")
        bets = await bets_collection.find({"odds": {"$lt": odds}}).to_list(length=None)
        return bets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bets by odds: {str(e)}")
