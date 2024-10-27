# app/services/match.py
from bson import ObjectId
from models.match import Match
from schemas.match import MatchCreate, MatchUpdate
from db.mongodb import get_collection  # Ensure you have a way to access the collection

class MatchService:
    def __init__(self):
        # Use the get_collection function to access the "matches" collection
        self.collection = get_collection("matches")

    async def create_match(self, match: MatchCreate) -> Match:
        match_data = match.dict()
        new_match = await self.collection.insert_one(match_data)
        return Match(**match_data, id=str(new_match.inserted_id))  # Convert ObjectId to string

    async def get_all_matches(self) -> list[Match]:
        matches = await self.collection.find().to_list(length=100)
        return [Match(**match, id=str(match['_id'])) for match in matches]  # Convert ObjectId to string

    async def get_match_by_id(self, match_id: str) -> Match:
        match = await self.collection.find_one({"_id": ObjectId(match_id)})
        if match:
            return Match(**match, id=str(match['_id']))  # Convert ObjectId to string
        return None

    async def update_match(self, match_id: str, match: MatchUpdate) -> Match:
        updated_match = await self.collection.find_one_and_update(
            {"_id": ObjectId(match_id)},
            {"$set": match.dict()},
            return_document=True
        )
        if updated_match:
            return Match(**updated_match, id=str(updated_match['_id']))  # Convert ObjectId to string
        return None

    async def delete_match(self, match_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(match_id)})
        return result.deleted_count > 0
