from fastapi import APIRouter
from datetime import datetime, timezone
from app.schemas.weather import WeatherCreateRequest, WeatherRecordResponse
from app.core.database import weather_collection
from app.services.weather_api import fetch_real_weather

router = APIRouter(prefix="/weather", tags=["Weather CRUD"])

@router.post("/", response_model=WeatherRecordResponse)
async def create_weather_record(request: WeatherCreateRequest):
    
    real_location_name, real_temperatures = await fetch_real_weather(
        location=request.location,
        start_date=request.start_date,
        end_date=request.end_date
    )

    weather_document = {
        "location": real_location_name, 
        "start_date": request.start_date.isoformat(), 
        "end_date": request.end_date.isoformat(),
        "temperatures": [temp.model_dump(mode='json') for temp in real_temperatures],
        "created_at": datetime.now(timezone.utc)
    }

    result = await weather_collection.insert_one(weather_document)
    weather_document["_id"] = str(result.inserted_id)
    return weather_document