from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import database

router = APIRouter()

class MoodRequest(BaseModel):
    user_id: int
    mood: str
    

# Post mood data
@router.post("/mood")
async def track_mood(mood_request: MoodRequest):
    mood_data = {
        "user_id": mood_request.user_id,
        "mood": mood_request.mood
    }
    result = await database["moods"].insert_one(mood_data)  # Insert into MongoDB
    return {"message": "Mood saved successfully", "id": str(result.inserted_id)}

# Get mood data by user_id
@router.get("/mood/{user_id}")
async def get_mood(user_id: int):
    moods_cursor = await database["moods"].find({"user_id": user_id}).to_list(length=100)
    if not moods_cursor:
        raise HTTPException(status_code=404, detail="No moods found")
    
    # Convert ObjectId to string for each mood in the list
    for mood in moods_cursor:
        mood["_id"] = str(mood["_id"])  # Convert ObjectId to string
    
    return {"moods": moods_cursor}
