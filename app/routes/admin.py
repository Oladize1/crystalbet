from fastapi import APIRouter, HTTPException, status
from models import YourModel  # Import your models here
from database import MongoDBConnection  # Adjust the import according to your project structure
import logging

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)

@router.on_event("startup")
async def startup_event():
    """Run on app startup to connect to the database."""
    await MongoDBConnection.connect()

@router.on_event("shutdown")
async def shutdown_event():
    """Run on app shutdown to close the database connection."""
    await MongoDBConnection.close_connection()

@router.get("/")
async def read_admin():
    logger.info("Admin dashboard accessed")
    return {"message": "Welcome to the Admin Dashboard"}

@router.get("/items", response_model=list[YourModel])
async def get_items():
    """Retrieve items from the database."""
    try:
        db = MongoDBConnection.get_database()
        items = await db["items"].find().to_list(length=100)  # Adjust according to your collection
        return items
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch items")

@router.post("/items", response_model=YourModel)
async def create_item(item: YourModel):  # Ensure Pydantic model is created for validation
    """Create a new item."""
    try:
        db = MongoDBConnection.get_database()
        result = await db["items"].insert_one(item.dict())
        return {"id": str(result.inserted_id), **item.dict()}
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create item")
