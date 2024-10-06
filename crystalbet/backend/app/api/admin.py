from fastapi import APIRouter, HTTPException, status
from models.bet import Bet  # Ensure the Bet model is properly defined
from services.database import MongoDBConnection  # Ensure the database service is correct
from bson import ObjectId  # To handle MongoDB ObjectIDs
import logging

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Set log level to INFO or DEBUG

# Admin Dashboard Endpoint
@router.get("/")
async def read_admin():
    """Basic admin dashboard endpoint."""
    logger.info("Admin dashboard accessed")
    return {"message": "Welcome to the Admin Dashboard"}

# Retrieve All Bets from the Database
@router.get("/bets", response_model=list[Bet])
async def get_bets():
    """Retrieve all bets from the database."""
    try:
        db = MongoDBConnection.get_database()  # Retrieve the database instance
        bets = await db["bets"].find().to_list(length=100)  # Adjust collection name if necessary
        if not bets:
            logger.info("No bets found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bets found")
        return bets
    except Exception as e:
        logger.error(f"Error fetching bets: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Failed to fetch bets")

# Create a New Bet
@router.post("/bets", response_model=Bet)
async def create_bet(bet: Bet):
    """Create a new bet in the database."""
    try:
        db = MongoDBConnection.get_database()
        result = await db["bets"].insert_one(bet.dict())
        created_bet = {**bet.dict(), "id": str(result.inserted_id)}
        logger.info(f"Bet created with ID: {created_bet['id']}")
        return created_bet
    except Exception as e:
        logger.error(f"Error creating bet: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Failed to create bet")

# Retrieve a Bet by ID
@router.get("/bets/{bet_id}", response_model=Bet)
async def get_bet_by_id(bet_id: str):
    """Retrieve a bet by its ID."""
    try:
        db = MongoDBConnection.get_database()
        bet = await db["bets"].find_one({"_id": ObjectId(bet_id)})
        if not bet:
            logger.info(f"No bet found with ID: {bet_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found")
        return bet
    except Exception as e:
        logger.error(f"Error fetching bet with ID {bet_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Failed to fetch bet")

# Update a Bet by ID
@router.put("/bets/{bet_id}", response_model=Bet)
async def update_bet(bet_id: str, updated_bet: Bet):
    """Update a bet by its ID."""
    try:
        db = MongoDBConnection.get_database()
        result = await db["bets"].update_one({"_id": ObjectId(bet_id)}, {"$set": updated_bet.dict()})
        if result.matched_count == 0:
            logger.info(f"No bet found with ID: {bet_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found")
        logger.info(f"Bet with ID {bet_id} updated.")
        return {**updated_bet.dict(), "id": bet_id}
    except Exception as e:
        logger.error(f"Error updating bet with ID {bet_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Failed to update bet")

# Delete a Bet by ID
@router.delete("/bets/{bet_id}")
async def delete_bet(bet_id: str):
    """Delete a bet by its ID."""
    try:
        db = MongoDBConnection.get_database()
        result = await db["bets"].delete_one({"_id": ObjectId(bet_id)})
        if result.deleted_count == 0:
            logger.info(f"No bet found with ID: {bet_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found")
        logger.info(f"Bet with ID {bet_id} deleted.")
        return {"message": f"Bet with ID {bet_id} has been deleted"}
    except Exception as e:
        logger.error(f"Error deleting bet with ID {bet_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Failed to delete bet")
