import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection as Collection
from pymongo.errors import PyMongoError, DuplicateKeyError, NetworkTimeout
from bson import ObjectId
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import asyncio

# Load environment variables from a .env file
load_dotenv()

# Database connection parameters
MONGODB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "betting_db")

# Collection names
COLLECTIONS = {
    "sports": "sports",
    "bets": "bets",
    "users": "users",
    "live_bets": "live_bets",
    "live_streams": "live_streams",
    "coupons": "coupons",
    "events": "events"
}

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB Connection Class
class MongoDBConnection:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri, maxPoolSize=10, minPoolSize=1)
        self.db = self.client[db_name]
        # Create indexes asynchronously
        asyncio.create_task(self.create_indexes())

    async def close(self):
        """Close the MongoDB connection."""
        self.client.close()
        logger.info("MongoDB connection closed.")

    async def create_indexes(self):
        """Create indexes for collections."""
        try:
            await self.db[COLLECTIONS["users"]].create_index("email", unique=True)
            await self.db[COLLECTIONS["users"]].create_index("username", unique=True)
            await self.db[COLLECTIONS["bets"]].create_index("user_id")
            await self.db[COLLECTIONS["live_bets"]].create_index("user_id")
            await self.db[COLLECTIONS["sports"]].create_index("category")
            logger.info("Indexes created successfully.")
        except PyMongoError as e:
            logger.error(f"Error creating indexes: {e}")

mongo_db_connection = MongoDBConnection(MONGODB_URI, DATABASE_NAME)

# Dependency to get the database
@asynccontextmanager
async def get_db():
    """Provide a database connection."""
    try:
        yield mongo_db_connection.db
    finally:
        await mongo_db_connection.close()

# Helper function to convert ObjectId to string
def convert_object_id_to_str(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert ObjectId to string for JSON serialization."""
    if "_id" in data and isinstance(data["_id"], ObjectId):
        data["_id"] = str(data["_id"])
    return data

# Helper function to convert lists of documents
def convert_list_of_object_ids_to_str(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert ObjectIds to strings in a list of documents."""
    return [convert_object_id_to_str(item) for item in data]

# Define the custom DatabaseError exception
class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    def __init__(self, message: str):
        super().__init__(message)

# Error handling middleware
def database_error_handler(func):
    """Decorator to handle database errors."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error: {str(e)}")
            raise DatabaseError("Duplicate key error occurred.")
        except NetworkTimeout as e:
            logger.error(f"Network timeout error: {str(e)}")
            raise DatabaseError("Database timeout error.")
        except PyMongoError as e:
            logger.error(f"MongoDB error: {str(e)}")
            raise DatabaseError("A general database error occurred.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception("An unexpected error occurred.")
    return wrapper

# Pydantic models for validation
class UserModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^\S+@\S+\.\S+$')  # Updated to use 'pattern'
    password: str = Field(..., min_length=6)
    username: str = Field(..., min_length=3, max_length=20)

class BetModel(BaseModel):
    user_id: str
    amount: float
    game: str
    odds: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Password hashing functions
class PasswordManager:
    from passlib.context import CryptContext

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

password_manager = PasswordManager()

# --- User Registration ---
@database_error_handler
async def register_user(users_collection: Collection, user_data: UserModel) -> Dict[str, Any]:
    """Register a new user."""
    user_dict = user_data.dict()
    
    # Hash the user's password before storing it
    user_dict['password'] = password_manager.hash_password(user_dict['password'])
    
    # Insert the new user into the database
    new_user = await users_collection.insert_one(user_dict)
    
    # Log the success and return the inserted user ID
    logger.info(f"Registered new user with ID {new_user.inserted_id}")
    
    # Return the ID of the newly registered user
    return {"_id": str(new_user.inserted_id)}

# --- User Login ---
@database_error_handler
async def login_user(db: Collection, email: str, password: str) -> Optional[Dict[str, Any]]:
    """Log in a user."""
    users_collection = db[COLLECTIONS["users"]]
    user = await users_collection.find_one({"email": email})
    if user and password_manager.verify_password(password, user['password']):
        logger.info(f"User {email} logged in successfully.")
        return convert_object_id_to_str(user)
    else:
        logger.warning(f"Failed login attempt for email: {email}")
        return None

# --- Fetch All Bets ---
@database_error_handler
async def fetch_all_bets(db: Collection, limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
    """Fetch all bets with pagination."""
    bets_collection = db[COLLECTIONS["bets"]]
    bets_cursor = bets_collection.find({}).skip(skip).limit(limit)
    bets = await bets_cursor.to_list(length=limit)
    logger.info(f"Fetched {len(bets)} bets")
    return convert_list_of_object_ids_to_str(bets)

# --- Fetch User Profile ---
@database_error_handler
async def fetch_user_profile(db: Collection, user_id: str) -> Optional[Dict[str, Any]]:
    """Fetch user profile information."""
    users_collection = db[COLLECTIONS["users"]]
    user_profile = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user_profile:
        user_profile.pop('password', None)  # Remove password from the returned data
        logger.info(f"Fetched profile for user {user_id}")
        return convert_object_id_to_str(user_profile)
    else:
        logger.warning(f"User profile not found for user {user_id}")
        return None

# --- Update User Profile ---
@database_error_handler
async def update_user_profile(db: Collection, user_id: str, update_data: Dict[str, Any]) -> bool:
    """Update user profile information."""
    users_collection = db[COLLECTIONS["users"]]
    if 'password' in update_data:
        update_data['password'] = password_manager.hash_password(update_data['password'])
    result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.modified_count > 0:
        logger.info(f"Updated user profile for {user_id}")
        return True
    else:
        logger.warning(f"No changes made to user profile for {user_id}")
        return False

# --- Fetch Sports Categories ---
@database_error_handler
async def fetch_sports_categories(db: Collection) -> List[str]:
    """Fetch all sports categories."""
    sports_collection = db[COLLECTIONS["sports"]]
    categories = await sports_collection.distinct("category")
    logger.info(f"Fetched sports categories: {categories}")
    return categories

# --- Fetch Sports by Category ---
@database_error_handler
async def fetch_sports_by_categories(db: Collection, category: str) -> List[Dict[str, Any]]:
    """Fetch sports by category."""
    sports_collection = db[COLLECTIONS["sports"]]
    sports = await sports_collection.find({"category": category}).to_list(length=100)
    logger.info(f"Fetched {len(sports)} sports for category: {category}")
    return convert_list_of_object_ids_to_str(sports)

# Example of using the connection and functions
async def main():
    async with get_db() as db:
        # Example usage of functions
        user_data = UserModel(name="John Doe", email="john@example.com", password="securepassword", username="johndoe")
        await register_user(db[COLLECTIONS["users"]], user_data)
        user_profile = await fetch_user_profile(db[COLLECTIONS["users"]], "user_id_here")
        print(user_profile)

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
