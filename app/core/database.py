from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)

db = client.weather_app_db
weather_collection = db.get_collection("weather_records")