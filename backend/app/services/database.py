from typing import Any, Dict, List, Optional
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient  # Async MongoDB driver
from fastapi import HTTPException

class DatabaseService:
    def __init__(self, db_client: AsyncIOMotorClient, db_name: str):
        self.db = db_client[db_name]

    # User Operations (Auth & Profile)
    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user in the database."""
        existing_user = await self.db.users.find_one({"email": user_data['email']})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        result = await self.db.users.insert_one(user_data)
        return str(result.inserted_id)

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find a user by their email address."""
        user = await self.db.users.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return user

    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update the user's profile information."""
        result = await self.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        return result.modified_count > 0

    # Bet Operations
    async def create_bet(self, bet_data: Dict[str, Any]) -> str:
        """Create a new bet."""
        result = await self.db.bets.insert_one(bet_data)
        return str(result.inserted_id)

    async def get_bet(self, bet_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve bet by ID."""
        bet = await self.db.bets.find_one({"_id": ObjectId(bet_id)})
        if bet:
            bet['_id'] = str(bet['_id'])
        return bet

    async def get_bets(self, filter_query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """Retrieve all bets or filter based on query."""
        bets = self.db.bets.find(filter_query)
        return [{"_id": str(bet['_id']), **bet} async for bet in bets]

    # Match Operations
    async def get_match(self, match_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve match by ID."""
        match = await self.db.matches.find_one({"_id": ObjectId(match_id)})
        if match:
            match['_id'] = str(match['_id'])
        return match

    async def get_live_matches(self) -> List[Dict[str, Any]]:
        """Retrieve live matches."""
        live_matches = self.db.matches.find({"is_live": True})
        return [{"_id": str(match['_id']), **match} async for match in live_matches]

    async def get_today_events(self) -> List[Dict[str, Any]]:
        """Retrieve today's events."""
        from datetime import datetime
        today = datetime.now().date()
        today_events = self.db.matches.find({"event_date": today})
        return [{"_id": str(event['_id']), **event} async for event in today_events]

    # Casino Operations
    async def get_casino_games(self) -> List[Dict[str, Any]]:
        """Retrieve a list of casino games."""
        games = self.db.casino.find()
        return [{"_id": str(game['_id']), **game} async for game in games]

    async def get_live_casino_games(self) -> List[Dict[str, Any]]:
        """Retrieve live casino games."""
        live_games = self.db.casino.find({"is_live": True})
        return [{"_id": str(game['_id']), **game} async for game in live_games]

    # Virtual Sports Operations
    async def get_virtual_sports(self) -> List[Dict[str, Any]]:
        """Retrieve a list of virtual sports."""
        virtual_sports = self.db.virtuals.find()
        return [{"_id": str(sport['_id']), **sport} async for sport in virtual_sports]

    # Coupon Operations
    async def validate_coupon(self, coupon_code: str) -> Optional[Dict[str, Any]]:
        """Validate a betting coupon."""
        coupon = await self.db.coupons.find_one({"code": coupon_code})
        if coupon and coupon['is_valid']:
            return coupon
        raise HTTPException(status_code=400, detail="Invalid or expired coupon")

    # Payment Operations
    async def initiate_payment(self, payment_data: Dict[str, Any]) -> str:
        """Initiate a new payment."""
        result = await self.db.payments.insert_one(payment_data)
        return str(result.inserted_id)

    async def verify_payment(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Verify payment by payment ID."""
        payment = await self.db.payments.find_one({"_id": ObjectId(payment_id)})
        if payment:
            payment['_id'] = str(payment['_id'])
        return payment

    # Transaction Operations
    async def get_transactions(self, filter_query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """Retrieve all transactions or filter based on query."""
        transactions = self.db.transactions.find(filter_query)
        return [{"_id": str(transaction['_id']), **transaction} async for transaction in transactions]

    async def get_transaction_by_id(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve transaction by ID."""
        transaction = await self.db.transactions.find_one({"_id": ObjectId(transaction_id)})
        if transaction:
            transaction['_id'] = str(transaction['_id'])
        return transaction
    # Bet Operations
async def get_all_bets(self) -> List[Dict[str, Any]]:
    """Retrieve all bets in the collection."""
    bets_cursor = self.db.bets.find()  # No filter means get all bets
    bets = []
    async for bet in bets_cursor:
        bet['_id'] = str(bet['_id'])  # Convert ObjectId to string
        bets.append(bet)
    return bets
