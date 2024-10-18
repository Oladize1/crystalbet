from pydantic import BaseModel, Field,ConfigDict
from typing import Optional

class AdminContentBase(BaseModel):
    title: str = Field(..., example="Sample Title")
    description: str = Field(..., example="Sample Description")

class AdminContentCreate(AdminContentBase):
    pass

class AdminContentUpdate(AdminContentBase):
    pass

class AdminContent(AdminContentBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
