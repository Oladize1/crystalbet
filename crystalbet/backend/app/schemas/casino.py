# schemas/casino.py

from pydantic import BaseModel, Field,ConfigDict
from typing import List, Optional

class CasinoGameCreate(BaseModel):
    name: str
    category: str
    provider: str
    description: str
    is_live: bool

class CasinoGameResponse(BaseModel):
    id: str
    name: str
    category: str
    provider: str
    description: str
    is_live: bool

    class Config:
        from_attributes = True

class CasinoGamesResponse(BaseModel):
    games: List[CasinoGameResponse]
