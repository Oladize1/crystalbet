from pydantic import BaseModel, Field, validator
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

# Reuse the BetSelection class from the original Bet schema
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

# The main Bet schema
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

# QuickBetSchema for a lightweight version of the Bet schema
class QuickBetSchema(BaseModel):
    user_id: str = Field(..., description="ID of the user placing the bet")
    selections: List[BetSelection] = Field(..., description="List of selections made by the user")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345",
                "selections": [
                    {
                        "match_id": "67890",
                        "bet_amount": 100.0,
                        "bet_type": BetType.WIN,
                        "odds": 2.5
                    }
                ]
            }
        }

# BookBetSchema for a detailed version of the Bet schema
class BookBetSchema(BaseModel):
    user_id: str = Field(..., description="ID of the user placing the bet")
    selections: List[BetSelection] = Field(..., description="List of selections made by the user")
    booking_code: Optional[str] = Field(None, description="Unique booking code for the bet")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345",
                "selections": [
                    {
                        "match_id": "67890",
                        "bet_amount": 100.0,
                        "bet_type": BetType.WIN,
                        "odds": 2.5
                    }
                ],
                "booking_code": "BOOK123"
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
