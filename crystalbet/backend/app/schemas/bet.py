from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum
from datetime import datetime


# Define an Enum for bet types with descriptions
class BetType(str, Enum):
    WIN = "win"
    LOSE = "lose"

    def __str__(self):
        return self.value.capitalize()


# Enum for bet results
class BetResult(str, Enum):
    WON = "won"
    LOST = "lost"
    PENDING = "pending"

    def __str__(self):
        return self.value.capitalize()


# Schema for individual bet details
class BetDetailSchema(BaseModel):
    match_id: str = Field(..., min_length=1, description="The ID of the match for the bet")
    bet_amount: float = Field(..., gt=0, description="The amount of money being bet (must be greater than zero)")
    bet_type: BetType = Field(..., description="Type of bet (e.g., 'win' or 'lose')")
    odds: float = Field(..., gt=0, description="Odds for the bet (must be greater than zero)")

    class Config:
        json_schema_extra = {
            "example": {
                "match_id": "67890",
                "bet_amount": 50.0,
                "bet_type": BetType.WIN,
                "odds": 1.8
            }
        }


# Schema for quick bet
class QuickBetSchema(BaseModel):
    user_id: str = Field(..., min_length=1, description="ID of the user placing the bet")
    match_id: str = Field(..., min_length=1, description="The ID of the match to bet on")
    bet_amount: float = Field(..., gt=0, description="The amount of money to bet (must be greater than zero)")
    bet_type: BetType = Field(..., description="Type of bet (e.g., 'win' or 'lose')")
    odds: float = Field(..., gt=0, description="Odds for the bet (must be greater than zero)")
    potential_win: Optional[float] = Field(default=None, description="Potential winnings based on the odds")

    @validator('potential_win', pre=True, always=True)
    def calculate_potential_win(cls, v, values):
        """Calculate potential winnings if not provided"""
        if v is None and 'bet_amount' in values and 'odds' in values:
            return values['bet_amount'] * values['odds']
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "12345",
                "match_id": "67890",
                "bet_amount": 100.0,
                "bet_type": BetType.WIN,
                "odds": 2.5,
                "potential_win": 250.0  # This will be calculated if omitted
            }
        }


# Schema for booking a bet
class BookBetSchema(BaseModel):
    booking_code: str = Field(..., min_length=1, description="Unique booking code for the bet")
    user_id: str = Field(..., min_length=1, description="ID of the user booking the bet")
    bet_details: List[BetDetailSchema] = Field(..., description="List of bet details")

    @validator('bet_details')
    def validate_bet_details(cls, value):
        """Ensure that there is at least one bet detail in the list"""
        if len(value) < 1:
            raise ValueError("bet_details must contain at least one bet detail.")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "booking_code": "BOOK123",
                "user_id": "12345",
                "bet_details": [
                    {
                        "match_id": "67890",
                        "bet_amount": 50.0,
                        "bet_type": BetType.WIN,
                        "odds": 1.8
                    },
                    {
                        "match_id": "12345",
                        "bet_amount": 20.0,
                        "bet_type": BetType.LOSE,
                        "odds": 3.0
                    }
                ]
            }
        }


# Schema for bet history
class BetHistorySchema(BaseModel):
    bet_id: str = Field(..., min_length=1, description="Unique ID of the bet")
    user_id: str = Field(..., min_length=1, description="ID of the user who placed the bet")
    match_id: str = Field(..., min_length=1, description="ID of the match related to the bet")
    bet_amount: float = Field(..., gt=0, description="The amount of money bet (must be greater than zero)")
    bet_type: BetType = Field(..., description="Type of bet (e.g., 'win' or 'lose')")
    odds: float = Field(..., gt=0, description="Odds for the bet (must be greater than zero)")
    result: BetResult = Field(..., description="The result of the bet (won, lost, pending)")
    potential_win: Optional[float] = Field(default=None, description="Potential winnings based on the bet odds")
    timestamp: datetime = Field(..., description="Time the bet was placed")

    @validator('potential_win', pre=True, always=True)
    def calculate_potential_win(cls, v, values):
        """Calculate potential winnings if not provided"""
        if v is None and 'bet_amount' in values and 'odds' in values:
            return values['bet_amount'] * values['odds']
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "bet_id": "BET12345",
                "user_id": "12345",
                "match_id": "67890",
                "bet_amount": 100.0,
                "bet_type": BetType.WIN,
                "odds": 2.5,
                "result": BetResult.WON,
                "potential_win": 250.0,
                "timestamp": "2024-09-28T12:34:56Z"
            }
        }


# Schema for general bet response
class BetResponseSchema(BaseModel):
    status: str = Field(..., description="Status of the request (e.g., 'success', 'error')")
    message: str = Field(..., description="Human-readable message providing additional information")
    bet_history: Optional[BetHistorySchema] = Field(None, description="Detailed bet information, if applicable")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Bet placed successfully",
                "bet_history": {
                    "bet_id": "BET12345",
                    "user_id": "12345",
                    "match_id": "67890",
                    "bet_amount": 100.0,
                    "bet_type": BetType.WIN,
                    "odds": 2.5,
                    "result": BetResult.WON,
                    "potential_win": 250.0,
                    "timestamp": "2024-09-28T12:34:56Z"
                }
            }
        }


# Schema for an error response
class ErrorResponseSchema(BaseModel):
    status: str = Field(..., description="Status of the request (should be 'error')")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[str] = Field(None, description="Optional additional details about the error")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Insufficient balance to place bet",
                "details": "Your account balance is 50.0, but the required bet amount is 100.0."
            }
        }
