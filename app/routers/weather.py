from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from typing import List
from bson import ObjectId
from app.schemas.weather import WeatherCreateRequest, WeatherRecordResponse, WeatherUpdateRequest
from app.core.database import weather_collection
from app.services.weather_api import fetch_real_weather

router = APIRouter(prefix="/weather", tags=["Weather CRUD"])

# ==========================================
# --- CREATE (C) ---
# ==========================================

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


# ==========================================
# --- READ (R) ---
# ==========================================

@router.get("/", response_model=List[WeatherRecordResponse])
async def get_all_weather_records():
    cursor = weather_collection.find({}).limit(100)
    records = await cursor.to_list(length=100)
    
    return records


@router.get("/{record_id}", response_model=WeatherRecordResponse)
async def get_weather_record_by_id(record_id: str):
    if not ObjectId.is_valid(record_id):
        raise HTTPException(status_code=400, detail="O ID fornecido é inválido.")
        
    record = await weather_collection.find_one({"_id": ObjectId(record_id)})
    
    if not record:
        raise HTTPException(status_code=404, detail="Registo de clima não encontrado.")
        
    return record


# ==========================================
# --- UPDATE (U) ---
# ==========================================

@router.put("/{record_id}", response_model=WeatherRecordResponse)
async def update_weather_record(record_id: str, request: WeatherUpdateRequest):
    if not ObjectId.is_valid(record_id):
        raise HTTPException(status_code=400, detail="O ID fornecido é inválido.")

    existing_record = await weather_collection.find_one({"_id": ObjectId(record_id)})
    if not existing_record:
        raise HTTPException(status_code=404, detail="Registo de clima não encontrado para atualização.")
    _, new_temperatures = await fetch_real_weather(
        location=existing_record["location"], 
        start_date=request.start_date,
        end_date=request.end_date
    )

    update_data = {
        "start_date": request.start_date.isoformat(),
        "end_date": request.end_date.isoformat(),
        "temperatures": [temp.model_dump(mode='json') for temp in new_temperatures]
    }

    updated_record = await weather_collection.find_one_and_update(
        {"_id": ObjectId(record_id)},
        {"$set": update_data},
        return_document=True
    )

    return updated_record


# ==========================================
# --- DELETE (D) ---
# ==========================================

@router.delete("/{record_id}")
async def delete_weather_record(record_id: str):
    if not ObjectId.is_valid(record_id):
        raise HTTPException(status_code=400, detail="O ID fornecido é inválido.")

    result = await weather_collection.delete_one({"_id": ObjectId(record_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Registo de clima não encontrado para exclusão.")

    return {"message": "Registo eliminado com sucesso!"}