from pydantic import BaseModel, Field, model_validator, BeforeValidator
from datetime import date, datetime
from typing import List, Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]

class WeatherCreateRequest(BaseModel):
    location: str = Field(..., description="Zip Code, Town, City, Landmarks, etc.")
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def check_date_range(self) -> 'WeatherCreateRequest':
        if self.start_date > self.end_date:
            raise ValueError('The start date cannot be later than the end date.')
        return self

class DailyTemperature(BaseModel):
    date: date
    temp_celsius: float
    description: str

class IntegrationsData(BaseModel):
    google_maps_url: str
    wikipedia_summary: Optional[str] = None
    youtube_videos: List[str] = []

class WeatherRecordResponse(BaseModel):
    id: PyObjectId = Field(alias="_id") 
    location: str
    start_date: date
    end_date: date
    temperatures: List[DailyTemperature]
    integrations: Optional[IntegrationsData] = None
    created_at: datetime

class WeatherUpdateRequest(BaseModel):
    location: Optional[str] = Field(None, description="New searched location (optional)")
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def check_date_range(self) -> 'WeatherUpdateRequest':
        if self.start_date > self.end_date:
            raise ValueError('The new start date cannot be later than the end date.')
        return self