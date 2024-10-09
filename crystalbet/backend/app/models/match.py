#models match.py
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List

class MatchModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    team_a: str
    team_b: str
    date: str  # Use ISO 8601 format (e.g., "2024-10-01T14:30:00Z")
    venue: str
    status: str  # e.g., "scheduled", "ongoing", "completed"

    class Config:
        # Use the alias for MongoDB ObjectId
        arbitrary_types_allowed = True
