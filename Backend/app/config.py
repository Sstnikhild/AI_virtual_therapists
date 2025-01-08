import motor.motor_asyncio
from urllib.parse import quote_plus


# MongoDB configuration
username = quote_plus('nikhildubey183')
password = quote_plus('N1i2k3h4i5l6@')

class Config:
    MONGO_URI = f"mongodb+srv://{username}:{password}@cluster.mw4vj.mongodb.net/AI_Virtual?retryWrites=true&w=majority"
    SECRET_KEY = "your_secret_key_here"
    DEBUG = True

# MongoDB Async client setup
client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)  # Use Config.MONGO_URI
database = client.get_database()  # Access the AI_Virtual database
