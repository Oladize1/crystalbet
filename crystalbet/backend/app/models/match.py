from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, Dict
from datetime import datetime

class Match(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    home_team: str
    away_team: str
    start_time: datetime  # Use datetime for proper time representation
    sport: str
    league: str
    odds: Dict[str, float]  # A dictionary for various betting odds, with string keys and float values

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for JSON serialization
        }

# Example usage
if __name__ == "__main__":
    match_example = Match(
        home_team="Team A",
        away_team="Team B",
        start_time=datetime(2024, 12, 31, 15, 0),  # Example datetime
        sport="Soccer",
        league="Premier League",
        odds={"win": 1.5, "draw": 3.0, "loss": 2.5}
    )
    
    print(match_example.json())  # Serialize to JSON
