from models.user import user_helper
from db.mongodb import get_collection
from schemas.user import UserUpdate
from bson import ObjectId

# Get the user profile by user ID
async def get_user_profile(user_id: str):
    db = get_collection("users")  # Get the database connection for the "users" collection
    user = await db.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)
    return None

# Update the user profile with the given user ID and updated data
async def update_user_profile(user_id: str, user_update: UserUpdate):
    db = get_collection("users")  # Get the database connection for the "users" collection
    updated_user_data = {k: v for k, v in user_update.dict().items() if v is not None}
    
    update_result = await db.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user_data})

    if update_result.matched_count == 1:
        updated_user = await db.find_one({"_id": ObjectId(user_id)})
        return user_helper(updated_user)
    return None
