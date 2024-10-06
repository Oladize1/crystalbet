from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from models.bet import Bet  # Import appropriate model for your project
from database import MongoDBConnection  # Ensure correct database import
import logging

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)

# On app startup, connect to the database
@router.on_event("startup")
async def startup_event():
    await MongoDBConnection.connect()

# On app shutdown, close the database connection
@router.on_event("shutdown")
async def shutdown_event():
    await MongoDBConnection.close_connection()

# Admin Dashboard Endpoint
@router.get("/")
async def read_admin():
    """Basic admin dashboard endpoint."""
    logger.info("Admin dashboard accessed")
    return {"message": "Welcome to the Admin Dashboard"}

# Retrieve All Bets from the Database
@router.get("/bets", response_model=list[Bet])
async def get_bets():
    """Retrieve bets from the database."""
    try:
        db = MongoDBConnection.get_database()  # Retrieve the database instance
        bets = await db["bets"].find().to_list(length=100)  # Adjust collection name as necessary
        if not bets:
            logger.info("No bets found in the database.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bets found.")
        return bets
    except Exception as e:
        logger.error(f"Error fetching bets: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch bets")

# Create a New Bet
@router.post("/bets", response_model=Bet)
async def create_bet(bet: Bet):
    """Create a new bet and insert it into the database."""
    try:
        db = MongoDBConnection.get_database()  # Retrieve the database instance
        result = await db["bets"].insert_one(bet.dict())  # Insert the new bet
        created_bet = {**bet.dict(), "id": str(result.inserted_id)}  # Add the inserted ID to the response
        logger.info(f"Bet created with ID: {created_bet['id']}")
        return created_bet
    except Exception as e:
        logger.error(f"Error creating bet: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create bet")

# Delete a Bet (Optional for Admins)
@router.delete("/bets/{bet_id}")
async def delete_bet(bet_id: str):
    """Delete a bet by its ID."""
    try:
        db = MongoDBConnection.get_database()
        result = await db["bets"].delete_one({"_id": bet_id})
        if result.deleted_count == 0:
            logger.info(f"No bet found with ID: {bet_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found.")
        logger.info(f"Bet with ID {bet_id} deleted.")
        return {"message": f"Bet with ID {bet_id} has been deleted"}
    except Exception as e:
        logger.error(f"Error deleting bet: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete bet")
