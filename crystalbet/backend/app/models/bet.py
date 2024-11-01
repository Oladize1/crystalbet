# models/bet.py (MongoDB Models for Bet)

from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
from db.mongodb import get_db

class Bet(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    match_id: str
    bet_amount: float
    potential_win: float
    odds: float
    is_live: bool
    bet_status: str = "pending"  # Can be "pending", "won", "lost"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Pydantic v2 settings
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={ObjectId: str}  # Convert ObjectId to string in JSON responses
    )

    @classmethod
    async def create(cls, bet_data: dict):
        result = await get_db["bets"].insert_one(bet_data)
        return cls(**bet_data)

    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 10):
        bets = await get_db["bets"].find().skip(skip).limit(limit).to_list(length=limit)
        return [cls(**bet) for bet in bets]

    @classmethod
    async def get_by_user_id(cls, user_id: str):
        bets = await get_db["bets"].find({"user_id": user_id}).to_list(length=100)
        return [cls(**bet) for bet in bets]

    @classmethod
    async def get_by_odds(cls, max_odds: float):
        bets = await get_db["bets"].find({"odds": {"$lt": max_odds}}).to_list(length=100)
        return [cls(**bet) for bet in bets]

    @classmethod
    async def get_live_bets(cls):
        live_bets = await get_db["bets"].find({"is_live": True}).to_list(length=100)
        return [cls(**bet) for bet in live_bets]

class BetInDB(Bet):
    db_specific_field: Optional[str] = None
