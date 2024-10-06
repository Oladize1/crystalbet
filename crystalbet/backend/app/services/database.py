from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
import logging
from bson import ObjectId

# Database connection parameters
MONGODB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "betting_db"

class MongoDBConnection:
    def __init__(self, url: str, db_name: str):
        self.client = AsyncIOMotorClient(url)
        self.db = self.client[db_name]
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def close(self):
        """Close the MongoDB connection."""
        self.client.close()
        self.logger.info("MongoDB connection closed.")

# Initialize the MongoDB client
mongo_db_connection = MongoDBConnection(MONGODB_URL, DATABASE_NAME)

# Dependency to get the database
async def get_db() -> Collection:
    """
    Dependency to provide a MongoDB database connection.
    """
    return mongo_db_connection.db

# Helper function to convert ObjectId to string
def convert_object_id_to_str(data: dict) -> dict:
    """
    Convert MongoDB ObjectId to string in the given dictionary.
    This is useful for returning data to the client.
    """
    if "_id" in data:
        data["_id"] = str(data["_id"])
    return data

# Helper function to convert a list of documents
def convert_list_of_object_ids_to_str(data: list) -> list:
    """
    Convert a list of MongoDB documents, changing ObjectId fields to strings.
    """
    return [convert_object_id_to_str(item) for item in data]
