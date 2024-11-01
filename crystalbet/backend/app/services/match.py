# services/match.py
from models.match import Match
from schemas.match import MatchResponse, MatchCreate, MatchUpdate
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from db.mongodb import get_db

class MatchService:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_all_matches(self):
        matches = []
        async for match in self.collection.find():
            matches.append(MatchResponse(**match))
        return matches

    async def get_match(self, match_id: str):
        match_data = await self.collection.find_one({"_id": ObjectId(match_id)})
        if match_data:
            return MatchResponse(**match_data)

    async def create_match(self, match_data: MatchCreate):
        match = Match.from_dict(match_data.dict())
        created_match = await MatchCreate(self.collection, match)
        return MatchResponse(**created_match)

    async def update_match(self, match_id: str, match_data: MatchUpdate):
        updated_match = await self.collection.find_one_and_update(
            {"_id": ObjectId(match_id)},
            {"$set": match_data.dict()},
            return_document=True
        )
        if updated_match:
            return MatchResponse(**updated_match)

    async def delete_match(self, match_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(match_id)})
        return result.deleted_count > 0
    async def update_match(self, match_id: str, match_data: dict):
        result = await self.collection.update_one({"_id": match_id}, {"$set": match_data})
        if result.matched_count == 0:
            return None
        return await self.get_match(match_id)