from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from models.match import MatchSchema, MatchUpdateSchema
from bson import ObjectId
from typing import List, Dict, Optional

# Database setup
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["betting_db"]
matches_collection = db["matches"]

# Create a new match
async def create_match(match_data: MatchSchema) -> Dict[str, str]:
    try:
        match_dict = match_data.dict()
        result = await matches_collection.insert_one(match_dict)
        return {"message": "Match created successfully", "match_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating match: {str(e)}")

# Fetch all matches
async def fetch_all_matches() -> List[Dict]:
    try:
        matches = await matches_collection.find().to_list(length=None)  # Adjust length if pagination is needed
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching matches: {str(e)}")

# Fetch match by ID
async def fetch_match_by_id(match_id: str) -> Dict:
    try:
        match = await matches_collection.find_one({"_id": ObjectId(match_id)})  # Convert match_id to ObjectId
        if match:
            return match
        else:
            raise HTTPException(status_code=404, detail="Match not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching match by ID: {str(e)}")

# Update a match by ID
async def update_match(match_id: str, match_update_data: MatchUpdateSchema) -> Dict[str, str]:
    try:
        match_dict = match_update_data.dict(exclude_unset=True)
        result = await matches_collection.update_one({"_id": ObjectId(match_id)}, {"$set": match_dict})
        
        if result.modified_count == 1:
            return {"message": "Match updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Match not found or no changes made")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating match: {str(e)}")

# Delete a match by ID
async def delete_match(match_id: str) -> Dict[str, str]:
    try:
        result = await matches_collection.delete_one({"_id": ObjectId(match_id)})
        if result.deleted_count == 1:
            return {"message": "Match deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Match not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting match: {str(e)}")

# Filter matches by category, team, or date
async def filter_matches(category: Optional[str] = None, team: Optional[str] = None, date: Optional[str] = None) -> List[Dict]:
    try:
        query = {}
        if category:
            query["category"] = category
        if team:
            query["teams"] = {"$in": [team]}  # Assuming teams are stored in a list
        if date:
            query["date"] = date

        matches = await matches_collection.find(query).to_list(length=None)  # Adjust length for pagination
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering matches: {str(e)}")

# Example: Find ongoing matches
async def fetch_ongoing_matches() -> List[Dict]:
    try:
        ongoing_matches = await matches_collection.find({"status": "ongoing"}).to_list(length=None)
        return ongoing_matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ongoing matches: {str(e)}")
