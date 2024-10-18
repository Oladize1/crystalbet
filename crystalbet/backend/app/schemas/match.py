# app/schemas/match.py

from pydantic import BaseModel, ConfigDict
from typing import Dict

class MatchCreate(BaseModel):
    home_team: str
    away_team: str
    start_time: str
    sport: str
    league: str
    odds: Dict[str, float]  # A dictionary for various betting odds

class MatchUpdate(BaseModel):
    home_team: str = None
    away_team: str = None
    start_time: str = None
    sport: str = None
    league: str = None
    odds: Dict[str, float] = None  # A dictionary for various betting odds

class MatchResponse(MatchCreate):
    id: str  # Returns the ObjectId as a string
