from pydantic import BaseModel

class Bet(BaseModel):
    user_id: str
    amount: float
    odds: float
    status: str
