# schemas/virtual.py

from pydantic import BaseModel, ConfigDict
from typing import Optional

class VirtualSportCreate(BaseModel):
    name: str
    description: str
    image_url: Optional[str]
    odds: dict

class VirtualSportResponse(BaseModel):
    id: str
    name: str
    description: str
    image_url: Optional[str]
    odds: dict

    class Config:
        from_attributes = True
