# services/virtual.py

from models.virtual import VirtualSport
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId

class VirtualSportService:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["your_database_name"]  # Replace with your database name
        self.collection = self.db["virtual_sports"]

    async def create_virtual_sport(self, virtual_sport: VirtualSport):
        sport_data = virtual_sport.dict()
        result = await self.collection.insert_one(sport_data)
        sport_data["_id"] = str(result.inserted_id)
        return VirtualSport(**sport_data)

    async def get_all_virtual_sports(self) -> List[VirtualSport]:
        sports_cursor = self.collection.find()
        sports = [VirtualSport(**sport) for sport in await sports_cursor.to_list(length=100)]
        return sports

    async def get_virtual_sport(self, sport_id: str) -> Optional[VirtualSport]:
        sport = await self.collection.find_one({"_id": ObjectId(sport_id)})
        if sport:
            return VirtualSport(**sport)
        return None
