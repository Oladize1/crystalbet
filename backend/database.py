import motor.motor_asyncio
from config import MONGO_URI, DATABASE_NAME, MAX_POOL_SIZE, MIN_POOL_SIZE
import logging
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
import asyncio

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
                # Added timeout to avoid indefinite waits
                cls._client = motor.motor_asyncio.AsyncIOMotorClient(
                    MONGO_URI,
                    serverSelectionTimeoutMS=5000,  # 5-second timeout for initial connection
                    maxPoolSize=MAX_POOL_SIZE,
                    minPoolSize=MIN_POOL_SIZE
                )
                # Try to ping the database to ensure the connection is successful
                await cls._client.admin.command('ping')
                cls._db = cls._client[DATABASE_NAME]
                cls._connected = True
                logger.info(f"Successfully connected to MongoDB database: {DATABASE_NAME}")

                # Ensure indexes are created for optimized performance
                await cls.create_user_id_index()

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
    async def create_user_id_index(cls):
        """Create an index on the 'user_id' field in the bet_history collection for optimized querying."""
        try:
            bet_history_collection = cls._db["bet_history"]
            # MongoDB manages index existence, but let's log accordingly
            index_name = await bet_history_collection.create_index([("user_id", 1)], unique=False)
            logger.info(f"Index ensured on 'user_id': {index_name}")
        except PyMongoError as e:
            logger.error(f"Failed to create index on 'user_id': {e}")
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

# Initialize MongoDB connection during app startup
async def init_db():
    retries = 3  # Retry connecting 3 times if it fails
    delay = 2  # Delay between retries

    for attempt in range(1, retries + 1):
        try:
            await MongoDBConnection.connect()
            break  # Exit loop if connection is successful
        except (ServerSelectionTimeoutError, PyMongoError) as e:
            logger.error(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                logger.info(f"Retrying MongoDB connection in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                logger.error("Exceeded maximum retries. MongoDB connection failed.")
                raise e
