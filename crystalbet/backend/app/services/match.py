from typing import List, Optional, Dict, Any
from backend.app.models import Match, Coupon  # Ensure your Match and Coupon models are imported
from services.database import db  # Adjust the import to your database module
import logging

logger = logging.getLogger("match_services")

async def create_match(match_details: Match) -> Match:
    try:
        match_data = match_details.dict()
        new_match = await db.matches.insert_one(match_data)
        logger.info(f"Match created with ID: {new_match.inserted_id}")
        return match_data  # Return the created match data
    except Exception as e:
        logger.error(f"Error creating match: {str(e)}")
        raise

async def fetch_matches() -> List[Match]:
    try:
        matches = await db.matches.find().to_list(length=None)  # Fetch all matches
        return matches
    except Exception as e:
        logger.error(f"Error fetching matches: {str(e)}")
        raise

async def update_match(match_id: str, updated_details: Dict[str, Any]) -> Optional[Match]:
    try:
        result = await db.matches.update_one({"match_id": match_id}, {"$set": updated_details})
        if result.modified_count > 0:
            logger.info(f"Match with ID {match_id} updated")
            return await fetch_match_by_id(match_id)
        else:
            logger.warning(f"No match found with ID: {match_id} to update")
            return None
    except Exception as e:
        logger.error(f"Error updating match: {str(e)}")
        raise

async def delete_match(match_id: str) -> bool:
    try:
        result = await db.matches.delete_one({"match_id": match_id})
        if result.deleted_count > 0:
            logger.info(f"Match with ID {match_id} deleted")
            return True
        else:
            logger.warning(f"No match found with ID: {match_id} to delete")
            return False
    except Exception as e:
        logger.error(f"Error deleting match: {str(e)}")
        raise

async def fetch_live_matches() -> List[Match]:
    try:
        live_matches = await db.matches.find({"status": "ongoing"}).to_list(length=None)
        return live_matches
    except Exception as e:
        logger.error(f"Error fetching live matches: {str(e)}")
        raise

async def fetch_match_by_id(match_id: str) -> Optional[Match]:
    try:
        match = await db.matches.find_one({"match_id": match_id})
        if not match:
            logger.warning(f"No match found with ID: {match_id}")
            return None
        return match
    except Exception as e:
        logger.error(f"Error fetching match by ID: {str(e)}")
        raise

async def fetch_sports_by_category(category: str) -> List[Match]:
    try:
        matches = await db.matches.find({"category": category}).to_list(length=None)
        return matches
    except Exception as e:
        logger.error(f"Error fetching matches for category {category}: {str(e)}")
        raise

async def fetch_live_stream(match_id: str) -> Optional[Dict[str, Any]]:
    try:
        stream_data = await db.live_streams.find_one({"match_id": match_id})
        if not stream_data:
            logger.warning(f"No live stream found for match ID: {match_id}")
            return None
        return stream_data
    except Exception as e:
        logger.error(f"Error fetching live stream for match ID {match_id}: {str(e)}")
        raise

async def fetch_casino_games() -> List[Dict[str, Any]]:
    try:
        games = await db.casino_games.find().to_list(length=None)
        return games
    except Exception as e:
        logger.error(f"Error fetching casino games: {str(e)}")
        raise

async def fetch_virtual_games() -> List[Dict[str, Any]]:
    try:
        virtuals = await db.virtual_games.find().to_list(length=None)
        return virtuals
    except Exception as e:
        logger.error(f"Error fetching virtual games: {str(e)}")
        raise

async def check_coupon(coupon_code: str) -> Optional[Coupon]:
    try:
        coupon = await db.coupons.find_one({"code": coupon_code})
        if not coupon:
            logger.warning(f"Coupon code not found: {coupon_code}")
            return None
        return coupon
    except Exception as e:
        logger.error(f"Error checking coupon code {coupon_code}: {str(e)}")
        raise
