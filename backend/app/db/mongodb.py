from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from fastapi import HTTPException
from typing import Any, List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DATABASE_NAME")

# Global MongoDB client
client: AsyncIOMotorClient = None
database = None

# Initialize MongoDB connection
async def init_db():
    global client, database
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        database = client[DB_NAME]
        print("Connected to MongoDB!")
    except PyMongoError as e:
        print(f"Could not connect to MongoDB: {e}")
        raise e

# Function to retrieve the database instance
def get_db():
    """Return the MongoDB database instance."""
    if database is None:
        raise HTTPException(status_code=500, detail="Database not initialized.")
    return database

# Function to retrieve a collection
def get_collection(collection_name: str):
    return database[collection_name]

# Helper functions for CRUD operations
# -----------------------------------------------------
async def find_one(collection: str, query: dict) -> dict:
    """Find a single document in the collection."""
    result = await get_collection(collection).find_one(query)
    if result:
        result['_id'] = str(result['_id'])  # Convert ObjectId to string
    return result

async def find_many(collection: str, query: dict = {}) -> List[dict]:
    """Find multiple documents in the collection."""
    cursor = get_collection(collection).find(query)
    results = []
    async for document in cursor:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
        results.append(document)
    return results

async def insert_one(collection: str, data: dict) -> str:
    """Insert a document into the collection."""
    result = await get_collection(collection).insert_one(data)
    return str(result.inserted_id)

async def insert_many(collection: str, data_list: List[dict]) -> List[str]:
    """Insert multiple documents into the collection."""
    result = await get_collection(collection).insert_many(data_list)
    return [str(inserted_id) for inserted_id in result.inserted_ids]

async def update_one(collection: str, query: dict, update_data: dict) -> bool:
    """Update a document in the collection."""
    result = await get_collection(collection).update_one(query, {"$set": update_data})
    return result.modified_count > 0

async def delete_one(collection: str, query: dict) -> bool:
    """Delete a document from the collection."""
    result = await get_collection(collection).delete_one(query)
    return result.deleted_count > 0

# Custom Helper for ObjectId
def is_valid_object_id(id_str: str) -> bool:
    """Check if a string is a valid MongoDB ObjectId."""
    try:
        ObjectId(id_str)
        return True
    except Exception:
        return False

# Get by ID (helper function)
async def get_by_id(collection: str, id: str) -> Any:
    """Retrieve a document by its ID."""
    if not is_valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ID format.")
    
    document = await find_one(collection, {"_id": ObjectId(id)})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    
    return document

# User CRUD
async def get_user_by_email(email: str) -> dict:
    return await find_one("users", {"email": email})

async def get_user_by_id(user_id: str) -> dict:
    return await get_by_id("users", user_id)

async def create_user(user_data: dict) -> str:
    return await insert_one("users", user_data)

async def update_user(user_id: str, update_data: dict) -> bool:
    return await update_one("users", {"_id": ObjectId(user_id)}, update_data)

# Bet CRUD
async def get_bet_by_id(bet_id: str) -> dict:
    return await get_by_id("bets", bet_id)

async def create_bet(bet_data: dict) -> str:
    return await insert_one("bets", bet_data)

async def update_bet(bet_id: str, update_data: dict) -> bool:
    return await update_one("bets", {"_id": ObjectId(bet_id)}, update_data)

async def delete_bet(bet_id: str) -> bool:
    return await delete_one("bets", {"_id": ObjectId(bet_id)})

# Close MongoDB connection
async def close_db():
    global client
    if client:
        client.close()
        print("Closed MongoDB connection.")
