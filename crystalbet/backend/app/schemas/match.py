from pydantic import BaseModel, Field
from typing import Dict, Optional, List

class MatchCreate(BaseModel):
    home_team: str
    away_team: str
    start_time: str
    sport: str
    league: str
    odds: Dict[str, float]  # A dictionary for various betting odds

class MatchUpdate(BaseModel):
    home_team: Optional[str] = Field(default=None)
    away_team: Optional[str] = Field(default=None)
    start_time: Optional[str] = Field(default=None)
    sport: Optional[str] = Field(default=None)
    league: Optional[str] = Field(default=None)
    odds: Optional[Dict[str, float]] = Field(default=None)  # A dictionary for various betting odds

class MatchResponse(MatchCreate):
    id: str  # Returns the ObjectId as a string

    class Config:
        # Allow population of model fields using their aliases (if any)
        populate_by_name = True
        json_encoders = {
            # Add custom encoders if needed
        }
class MatchCreate(BaseModel):
    home_team: str
    away_team: str
    start_time: str
    sport: str
    league: str
    odds: Dict[str, float]  # A dictionary for various betting odds

class MatchUpdate(BaseModel):
    home_team: Optional[str] = Field(default=None)
    away_team: Optional[str] = Field(default=None)
    start_time: Optional[str] = Field(default=None)
    sport: Optional[str] = Field(default=None)
    league: Optional[str] = Field(default=None)
    odds: Optional[Dict[str, float]] = Field(default=None)

class MatchDetailResponse(MatchCreate):
    id: str  # Match identifier
    status: str  # Additional field to indicate the match status

class MatchResponse(MatchCreate):
    id: str  # Returns the ObjectId as a string

    class Config:
        populate_by_name = True
        json_encoders = {
            # Add custom encoders if needed
        }

class LiveMatchResponse(MatchDetailResponse):
    live_updates: List[Dict[str, str]]  # List of live updates for a match

class SportCategoryResponse(BaseModel):
    category_id: str
    name: str
    description: Optional[str] = None