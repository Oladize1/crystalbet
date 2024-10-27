from typing import List, Optional
from models.admin import AdminContentModel
from schemas.admin import AdminContentCreate, AdminContentUpdate
from db.mongodb import init_db
from datetime import datetime
from bson import ObjectId
import logging

# Configure logger
logger = logging.getLogger(__name__)

class AdminService:
    def __init__(self, collection_name: str = "cms_content"):
        self.mongo_db = init_db()
        self.collection_name = collection_name

    async def get_all_content(self) -> List[AdminContentModel]:
        try:
            contents = await self.mongo_db[self.collection_name].find().to_list(length=100)
            return [AdminContentModel(id=str(content["_id"]), **content) for content in contents]
        except Exception as e:
            logger.error("Failed to retrieve all content: %s", e)
            raise

    async def get_content(self, content_id: str) -> Optional[AdminContentModel]:
        try:
            content = await self.mongo_db[self.collection_name].find_one({"_id": ObjectId(content_id)})
            if content:
                return AdminContentModel(id=str(content["_id"]), **content)
            return None
        except Exception as e:
            logger.error("Failed to retrieve content with id %s: %s", content_id, e)
            raise

    async def create_content(self, content: AdminContentCreate) -> AdminContentModel:
        new_content = content.dict()
        new_content["created_at"] = new_content["updated_at"] = datetime.utcnow()

        try:
            result = await self.mongo_db[self.collection_name].insert_one(new_content)
            new_content["id"] = str(result.inserted_id)
            return AdminContentModel(**new_content)
        except Exception as e:
            logger.error("Failed to create content: %s", e)
            raise

    async def update_content(self, content_id: str, content: AdminContentUpdate) -> Optional[AdminContentModel]:
        updated_content = content.dict(exclude_unset=True)
        updated_content["updated_at"] = datetime.utcnow()

        try:
            result = await self.mongo_db[self.collection_name].update_one({"_id": ObjectId(content_id)}, {"$set": updated_content})
            if result.modified_count == 0:
                logger.warning("No content modified with id %s", content_id)
                return None
            return await self.get_content(content_id)
        except Exception as e:
            logger.error("Failed to update content with id %s: %s", content_id, e)
            raise

    async def delete_content(self, content_id: str) -> bool:
        try:
            result = await self.mongo_db[self.collection_name].delete_one({"_id": ObjectId(content_id)})
            if result.deleted_count > 0:
                logger.info("Successfully deleted content with id %s", content_id)
            else:
                logger.warning("No content found to delete with id %s", content_id)
            return result.deleted_count > 0
        except Exception as e:
            logger.error("Failed to delete content with id %s: %s", content_id, e)
            raise
