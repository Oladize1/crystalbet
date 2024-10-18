from pydantic import BaseModel, ConfigDict
from typing import Optional
from bson import ObjectId

class AZMenuSchema(BaseModel):
    name: str
    url: str

class AZMenuResponse(AZMenuSchema):
    id: Optional[str]

    class Config:
        from_attributes = True
        json_encoders = {
            ObjectId: str
        }

class QuickLinksSchema(BaseModel):
    name: str
    url: str

class QuickLinksResponse(QuickLinksSchema):
    id: Optional[str]

    class Config:
        from_attributes = True
        json_encoders = {
            ObjectId: str
        }
