# services/casino.py

from motor.motor_asyncio import AsyncIOMotorClient
from models.casino import CasinoGame
from schemas.casino import CasinoGameCreate, CasinoGameResponse
from bson import ObjectId
from typing import List

class CasinoService:
    def __init__(self, db: AsyncIOMotorClient):
        self.collection = db.casino.games  # Assuming your MongoDB collection is named "games"

    async def create_game(self, game: CasinoGameCreate) -> CasinoGameResponse:
        game_dict = game.dict()
        result = await self.collection.insert_one(game_dict)
        game_dict["_id"] = str(result.inserted_id)
        return CasinoGameResponse(**game_dict)

    async def get_games(self) -> List[CasinoGameResponse]:
        games = []
        async for game in self.collection.find():
            games.append(CasinoGameResponse(**game))
        return games

    async def get_game(self, game_id: str) -> CasinoGameResponse:
        game = await self.collection.find_one({"_id": ObjectId(game_id)})
        if game:
            return CasinoGameResponse(**game)
        return None

    async def update_game(self, game_id: str, game: CasinoGameCreate) -> CasinoGameResponse:
        await self.collection.update_one({"_id": ObjectId(game_id)}, {"$set": game.dict()})
        return await self.get_game(game_id)

    async def delete_game(self, game_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(game_id)})
        return result.deleted_count > 0
