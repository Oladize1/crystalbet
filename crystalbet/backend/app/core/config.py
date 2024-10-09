# core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("config.log"),
    ]
)
logger = logging.getLogger(__name__)

# Pydantic settings class
class Settings(BaseSettings):
    ALLOW_ORIGINS: str
    TRUSTED_HOSTS: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MONGO_URI: str
    DATABASE_NAME: str
    MAX_POOL_SIZE: int
    MIN_POOL_SIZE: int

    class Config:
        env_file = ".env"

# Initialize the settings object
settings = Settings()

# Log configuration loading
logger.info(f"ALLOW_ORIGINS set to: {settings.ALLOW_ORIGINS}")
logger.info(f"TRUSTED_HOSTS set to: {settings.TRUSTED_HOSTS}")
logger.info("SECRET_KEY loaded successfully")
logger.info(f"ALGORITHM set to: {settings.ALGORITHM}")
logger.info(f"ACCESS_TOKEN_EXPIRE_MINUTES set to: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
logger.info(f"MONGO_URI set to: {settings.MONGO_URI}")
logger.info(f"DATABASE_NAME set to: {settings.DATABASE_NAME}")
logger.info(f"MAX_POOL_SIZE set to: {settings.MAX_POOL_SIZE}")
logger.info(f"MIN_POOL_SIZE set to: {settings.MIN_POOL_SIZE}")
logger.info("Configuration loaded successfully")

# Example usage of settings in the database connection
import motor.motor_asyncio

# Create a MongoDB client using the settings
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)

# Access the database
db = client[settings.DATABASE_NAME]
