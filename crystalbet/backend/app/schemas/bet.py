# schemas/bet.py (Pydantic Schemas for Request/Response Validation)

from pydantic import BaseModel, Field,ConfigDict
from typing import List, Optional
from datetime import datetime

class BetCreate(BaseModel):
    match_id: str
    bet_amount: float
    odds: float

class BetResponse(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    match_id: str
    bet_amount: float
    potential_win: float
    odds: float
    is_live: bool
    bet_status: str
    created_at: datetime

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

class BetSlipResponse(BaseModel):
    bets: List[BetResponse]
    total_bets: int
    total_amount: float
    total_potential_win: float

    class Config:
        from_attributes = True
