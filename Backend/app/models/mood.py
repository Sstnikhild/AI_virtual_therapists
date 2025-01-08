from pydantic import BaseModel

class Mood(BaseModel):
    user_id: int
    mood: str
    timestamp: str

