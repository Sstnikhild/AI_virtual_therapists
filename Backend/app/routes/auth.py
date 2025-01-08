from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.routes import security
from app.config import database  # Import the MongoDB database object

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

# Register Route
@router.post("/register")
async def register(user: User):
    # Hash the password before saving
    hashed_password = security.hash_password(user.password)
    
    # Create a user document
    user_document = {
        "username": user.username,
        "password": hashed_password
    }
    
    # Insert the user into the MongoDB collection
    users_collection = database["users"]  # Reference the 'users' collection
    existing_user = await users_collection.find_one({"username": user.username})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Insert the new user
    result = await users_collection.insert_one(user_document)
    
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

# Login Route
@router.post("/login")
async def login(user: User):
    # Fetch user from the database
    users_collection = database["users"]
    db_user = await users_collection.find_one({"username": user.username})
    
    if not db_user or not security.verify_password(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "token": "jwt_token_placeholder"}
