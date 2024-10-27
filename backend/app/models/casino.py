# models/casino.py

from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from typing import Optional
from datetime import datetime

class CasinoGame(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # Automatically generate ObjectId
    name: str
    category: str
    provider: str
    description: str
    is_live: bool
    created_at: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())

    # Pydantic v2 settings
    model_config = ConfigDict(
        from_attributes=True  # This enables the use of the field alias (e.g., "_id") when converting from MongoDB
    )
