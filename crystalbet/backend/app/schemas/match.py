from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Response models
class ResponseModel(BaseModel):
    message: str
    data: Dict[str, Any]

class ErrorResponseModel(BaseModel):
    detail: str

# Match schemas
class MatchSchema(BaseModel):
    match_id: Optional[str]
    team_a: str
    team_b: str
    date: str  # Use ISO 8601 format (e.g., "2024-10-01T14:30:00Z")
    venue: str
    status: str  # e.g., "scheduled", "ongoing", "completed"

class UpdateMatchSchema(BaseModel):
    match_id: str
    status: str
    date: Optional[str] = None
    venue: Optional[str] = None
