import motor.motor_asyncio
from core.config import settings
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
                    settings.MONGO_URI,
                    serverSelectionTimeoutMS=5000,
                    maxPoolSize=settings.MAX_POOL_SIZE,
                    minPoolSize=settings.MIN_POOL_SIZE
                )
                await cls._client.admin.command('ping')  # Check if MongoDB is reachable
                cls._db = cls._client[settings.DATABASE_NAME]
                cls._connected = True
                logger.info(f"Successfully connected to MongoDB database: {settings.DATABASE_NAME}")
                await cls.init_db()  # Initialize the database

            except (ServerSelectionTimeoutError, PyMongoError) as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise e
            except Exception as e:
                logger.exception("Unexpected error while connecting to MongoDB")
                raise e
        else:
            logger.info("MongoDB connection already established.")

    @classmethod
    def get_database(cls):
        """Return the MongoDB database instance."""
        if cls._db is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")
        return cls._db

    @classmethod
    async def ensure_indexes(cls):
        """Ensure necessary indexes for all collections."""
        try:
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
        """Initialize the MongoDB database by creating collections and indexes."""
        await cls.ensure_indexes()  # Ensure indexes exist
        try:
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
    async def fetch_quick_links(cls):
        """Fetch all quick links from the database."""
        try:
            quick_links_collection = cls.get_database()["quick_links"]
            result = await quick_links_collection.find().to_list(None)
            logger.info("Fetched quick links.")
            return result or []  # Return an empty list if no quick links found
        except PyMongoError as e:
            logger.error(f"Error fetching quick links: {e}")
            raise e

    @classmethod
    async def fetch_az_menu(cls):
        """Fetch all A-Z menu items from the database."""
        try:
            az_menu_collection = cls.get_database()["az_menu"]
            result = await az_menu_collection.find().to_list(None)
            logger.info("Fetched A-Z menu.")
            return result or []  # Return an empty list if no items found
        except PyMongoError as e:
            logger.error(f"Error fetching A-Z menu: {e}")
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
                logger.exception("Unexpected error while closing MongoDB")
                raise e
