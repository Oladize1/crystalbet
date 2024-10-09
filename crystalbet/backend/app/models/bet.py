#models/bet.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum


# Enum for BetType
class BetType(str, Enum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


# Enum for BetStatus
class BetStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Define LiveBet model
class LiveBet(BaseModel):
    user_id: str = Field(..., description="ID of the user placing the live bet")
    match_id: str = Field(..., description="ID of the match for the live bet")
    bet_amount: float = Field(..., gt=0, description="Amount of money bet")
    bet_type: BetType = Field(..., description="Type of bet, e.g., 'win', 'lose', or 'draw'")
    odds: float = Field(..., gt=0, description="The odds for this live bet")
    status: BetStatus = Field(..., description="Current status of the live bet")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "match_id": "match456",
                "bet_amount": 150.0,
                "bet_type": "win",
                "odds": 2.0,
                "status": "pending"
            }
        }


# BetSelection class for bet details
class BetSelection(BaseModel):
    match_id: str = Field(..., description="ID of the match for the selection")
    bet_amount: float = Field(..., gt=0, description="Amount of money bet")
    bet_type: BetType = Field(..., description="Type of bet, e.g., 'win' or 'lose'")
    odds: float = Field(..., gt=0, description="The odds for this selection")

    class Config:
        schema_extra = {
            "example": {
                "match_id": "67890",
                "bet_amount": 100.0,
                "bet_type": BetType.WIN,
                "odds": 2.5
            }
        }


# Main Bet schema
class Bet(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the bet")
    user_id: str = Field(..., description="ID of the user placing the bet")
    selections: List[BetSelection] = Field(..., description="List of selections made by the user")
    booking_code: Optional[str] = Field(None, description="Unique booking code for the bet")
    status: BetStatus = Field(..., description="Current status of the bet, e.g., 'pending', 'completed'")
    odds: float = Field(..., gt=0, description="The overall odds for the bet")

    class Config:
        schema_extra = {
            "example": {
                "id": "bet123",
                "user_id": "12345",
                "selections": [
                    {
                        "match_id": "67890",
                        "bet_amount": 100.0,
                        "bet_type": BetType.WIN,
                        "odds": 2.5
                    },
                    {
                        "match_id": "98765",
                        "bet_amount": 50.0,
                        "bet_type": BetType.LOSE,
                        "odds": 3.0
                    }
                ],
                "booking_code": "BOOK123",
                "status": BetStatus.PENDING,
                "odds": 1.8
            }
        }


# User model for user details
class User(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the user")
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email of the user")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    password: str = Field(..., description="Password for the user account")

    class Config:
        schema_extra = {
            "example": {
                "id": "user123",
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "password": "strongpassword123"
            }
        }


# GameSlot model to represent a game slot
class GameSlot(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the game slot")
    name: str = Field(..., description="Name of the game slot")
    category: str = Field(..., description="Category of the game")
    provider: str = Field(..., description="Provider of the game")
    description: str = Field(..., description="Description of the game")
    image_url: str = Field(..., description="URL of the game image")

    class Config:
        schema_extra = {
            "example": {
                "id": "slot123",
                "name": "Lucky Spin",
                "category": "Slots",
                "provider": "GameProvider Inc.",
                "description": "A thrilling slot game with exciting bonuses.",
                "image_url": "https://example.com/images/lucky-spin.jpg"
            }
        }


# Response model for game slot responses
class GameSlotResponse(BaseModel):
    name: str = Field(..., description="Name of the game slot")
    category: str = Field(..., description="Category of the game")
    provider: str = Field(..., description="Provider of the game")
    description: str = Field(..., description="Description of the game")
    image_url: str = Field(..., description="URL of the game image")


# QuickBetSchema for quick bets
class QuickBetSchema(BaseModel):
    user_id: str = Field(..., description="ID of the user placing the quick bet")
    game_id: str = Field(..., description="ID of the game or event being bet on")
    bet_amount: float = Field(..., gt=0, description="Amount being bet")
    odds: float = Field(..., gt=0, description="Odds for the bet")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "game_id": "game456",
                "bet_amount": 100.0,
                "odds": 2.5
            }
        }


# BookBetSchema for booking bets
class BookBetSchema(BaseModel):
    user_id: str = Field(..., description="ID of the user booking the bet")
    selections: List[QuickBetSchema] = Field(..., description="List of bet selections")
    booking_code: Optional[str] = Field(None, description="Unique booking code for the bet")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "selections": [
                    {
                        "game_id": "game456",
                        "bet_amount": 100.0,
                        "odds": 2.5
                    }
                ],
                "booking_code": "BOOK123"
            }
        }


# LiveBetSchema for live bets during events
class LiveBetSchema(BaseModel):
    user_id: str = Field(..., description="ID of the user placing the live bet")
    match_id: str = Field(..., description="ID of the live match being bet on")
    bet_amount: float = Field(..., gt=0, description="Amount being bet during the live event")
    odds: float = Field(..., gt=0, description="Live odds for the bet")
    status: BetStatus = Field(..., description="Current status of the live bet")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "match_id": "match456",
                "bet_amount": 150.0,
                "odds": 3.5,
                "status": BetStatus.PENDING
            }
        }


# Casino model
class Casino(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the casino")
    name: str = Field(..., description="Name of the casino")
    location: str = Field(..., description="Location of the casino")
    games_offered: List[str] = Field(..., description="List of games offered by the casino")
    description: str = Field(..., description="Description of the casino")

    class Config:
        schema_extra = {
            "example": {
                "id": "casino123",
                "name": "Big Win Casino",
                "location": "Las Vegas",
                "games_offered": ["Blackjack", "Poker", "Roulette"],
                "description": "A luxurious casino offering high-stakes games."
            }
        }


# Virtuals model
class Virtuals(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the virtual game")
    name: str = Field(..., description="Name of the virtual game")
    sport_type: str = Field(..., description="Type of sport in the virtual game")
    odds: float = Field(..., gt=0, description="Odds for betting on the virtual game")
    description: str = Field(..., description="Description of the virtual game")

    class Config:
        schema_extra = {
            "example": {
                "id": "virtual123",
                "name": "Virtual Soccer",
                "sport_type": "Soccer",
                "odds": 1.5,
                "description": "A simulated soccer game for betting."
            }
        }


# BetHistory model
class BetHistory(BaseModel):
    user_id: str = Field(..., description="ID of the user who placed the bet")
    bet_id: str = Field(..., description="ID of the bet placed")
    bet_amount: float = Field(..., gt=0, description="Amount of the bet")
    odds: float = Field(..., gt=0, description="Odds at which the bet was placed")
    status: BetStatus = Field(..., description="Status of the bet")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "bet_id": "bet456",
                "bet_amount": 50.0,
                "odds": 2.0,
                "status": BetStatus.COMPLETED
            }
        }


# CouponCheck model for checking bet coupons
class CouponCheck(BaseModel):
    user_id: str = Field(..., description="ID of the user checking the coupon")
    coupon_code: str = Field(..., description="Coupon code to check")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "coupon_code": "DISCOUNT10"
            }
        }


# Event model to represent events for betting
class Event(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the event")
    name: str = Field(..., description="Name of the event")
    date: str = Field(..., description="Date of the event")
    time: str = Field(..., description="Time of the event")
    location: str = Field(..., description="Location of the event")
    status: str = Field(..., description="Current status of the event")

    class Config:
        schema_extra = {
            "example": {
                "id": "event123",
                "name": "Championship Final",
                "date": "2024-10-15",
                "time": "18:00",
                "location": "National Stadium",
                "status": "scheduled"
            }
        }


# EventResponse model to represent event responses
class EventResponse(BaseModel):
    name: str = Field(..., description="Name of the event")
    date: str = Field(..., description="Date of the event")
    time: str = Field(..., description="Time of the event")
    location: str = Field(..., description="Location of the event")
    status: str = Field(..., description="Current status of the event")
# Function to retrieve all bets
def get_all_bets() -> List[Bet]:
    # This is where you would implement your database retrieval logic
    # For now, we will return an empty list as a placeholder
    return []