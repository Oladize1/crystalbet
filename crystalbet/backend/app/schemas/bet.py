from pydantic import BaseModel, Field
from typing import List, Optional

class BetCreate(BaseModel):
    match_id: str
    odds: float
    stake: float

class Bet(BaseModel):
    id: str
    match_id: str
    odds: float
    stake: float
    user_id: str
    status: str = Field(default="pending")  # default status

class BetOut(Bet):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class BetSlip(BaseModel):
    bets: List[Bet]
    total_stake: float
    potential_payout: float

class BetFilter(BaseModel):
    odds_less_than: Optional[float] = None
    status: Optional[str] = None
