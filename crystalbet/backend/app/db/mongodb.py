# services/database.py

import motor.motor_asyncio
from core.config import settings  # Ensure this path is correct
import logging
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBConnection:
    _client = None
    _db = None
    _connected = False

    @classmethod
    async def connect(cls):
        """Establish a connection to the MongoDB database."""
        if cls._client is None and not cls._connected:
            try:
                cls._client = motor.motor_asyncio.AsyncIOMotorClient(
                    settings.MONGO_URI,  # Ensure this is correctly set in your settings
                    serverSelectionTimeoutMS=5000,  # 5-second timeout for initial connection
                    maxPoolSize=settings.MAX_POOL_SIZE,
                    minPoolSize=settings.MIN_POOL_SIZE
                )
                # Ensure MongoDB is reachable
                await cls._client.admin.command('ping')
                cls._db = cls._client[settings.DATABASE_NAME]  # Use the database name from settings
                cls._connected = True
                logger.info(f"Connected to MongoDB database: {settings.DATABASE_NAME}")

                # Initialize the database (create collections and indexes)
                await cls.init_db()

            except ServerSelectionTimeoutError as e:
                logger.error(f"MongoDB connection timed out: {e}")
                raise e
            except PyMongoError as e:
                logger.error(f"PyMongo error occurred: {e}")
                raise e
            except Exception as e:
                logger.error(f"Unexpected error while connecting to MongoDB: {e}")
                raise e
        else:
            logger.info("MongoDB connection already established.")

    @classmethod
    def get_database(cls):
        """Get the MongoDB database instance."""
        if cls._db is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")
        return cls._db

    @classmethod
    async def ensure_indexes(cls):
        """Ensure necessary indexes for all collections."""
        try:
            # Ensure indexes for users, transactions, bets, etc.
            user_collection = cls._db["users"]
            await user_collection.create_index([("email", 1)], unique=True)

            bet_history_collection = cls._db["bet_history"]
            await bet_history_collection.create_index([("user_id", 1)], unique=False)

            transactions_collection = cls._db["transactions"]
            await transactions_collection.create_index([("user_id", 1)], unique=False)

            logger.info("Indexes ensured for collections.")

        except PyMongoError as e:
            logger.error(f"Failed to create indexes: {e}")
            raise e

    @classmethod
    async def init_db(cls):
        """Initialize the MongoDB database by creating necessary collections, indexes, and seed data."""
        try:
            # Ensure that indexes exist
            await cls.ensure_indexes()

            # Optionally, add seed data here (like a default admin user)
            user_collection = cls._db["users"]
            existing_admin = await user_collection.find_one({"email": "admin@example.com"})
            if not existing_admin:
                await user_collection.insert_one({
                    "email": "admin@example.com",
                    "password": "hashed_admin_password",  # Ensure this is hashed
                    "role": "admin",
                    "active": True
                })
                logger.info("Inserted default admin user.")
        except PyMongoError as e:
            logger.error(f"Failed to initialize the database: {e}")
            raise e

    @classmethod
    async def close_connection(cls):
        """Close the MongoDB connection."""
        if cls._client:
            try:
                cls._client.close()
                cls._connected = False
                logger.info("MongoDB connection closed.")
            except PyMongoError as e:
                logger.error(f"Error while closing MongoDB connection: {e}")
                raise e
            except Exception as e:
                logger.error(f"Unexpected error while closing MongoDB: {e}")
                raise e

# Test script (mongo.py)
import asyncio

async def main():
    try:
        await MongoDBConnection.connect()
    finally:
        await MongoDBConnection.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
