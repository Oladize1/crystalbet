# models/virtual.py

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class VirtualSport(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    description: str
    image_url: Optional[str]
    odds: dict  # Could be more structured depending on your requirements

    class Config:
        allow_population_by_field_name = True
