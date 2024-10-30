# app/services/bet.py

from pymongo.collection import Collection
from schemas.bet import Bet, BetCreate, BetSlip

class BetService:
    def __init__(self, db):
        self.collection: Collection = db["bets"]  # Replace with your actual collection name
        self.bet_slip_collection: Collection = db["bet_slips"]  # Collection for storing bet slips

    async def get_all_bets(self) -> list[Bet]:
        bets = await self.collection.find().to_list(length=None)
        return [Bet(**bet) for bet in bets]

    async def get_live_bets(self) -> list[Bet]:
        live_bets = await self.collection.find({"status": "live"}).to_list(length=None)
        return [Bet(**bet) for bet in live_bets]

    async def book_bet(self, bet: BetCreate, user_id: str) -> BetSlip:
        bet_data = bet.dict()
        bet_data["user_id"] = user_id  # Link the bet to the user
        result = await self.collection.insert_one(bet_data)
        bet_slip = BetSlip(**bet_data)  # Create a bet slip
        await self.bet_slip_collection.insert_one(bet_slip.dict())  # Save to bet slip collection
        return bet_slip

    async def get_bet_slip(self, user_id: str) -> BetSlip:
        bet_slip = await self.bet_slip_collection.find_one({"user_id": user_id})
        if bet_slip is None:
            raise ValueError("No bet slip found for this user.")
        return BetSlip(**bet_slip)
