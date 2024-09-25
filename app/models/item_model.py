# app/models/item_model.py
from pydantic import BaseModel, Field
from typing import Optional

class YourModel(BaseModel):
    name: str = Field(..., example="Item name")
    description: Optional[str] = Field(None, example="Item description")
    price: float = Field(..., gt=0, example=19.99)

    class Config:
        schema_extra = {
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item.",
                "price": 19.99
            }
        }
