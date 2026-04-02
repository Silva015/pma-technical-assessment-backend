from pydantic import BaseModel, Field, model_validator, BeforeValidator
from datetime import date, datetime
from typing import List, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class WeatherCreateRequest(BaseModel):
    location: str = Field(..., description="Zip Code, Town, City, Landmarks, etc.")
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def check_date_range(self) -> 'WeatherCreateRequest':
        if self.start_date > self.end_date:
            raise ValueError('A data inicial (start_date) não pode ser posterior à data final (end_date).')
        return self

class DailyTemperature(BaseModel):
    date: date
    temp_celsius: float
    description: str

class WeatherRecordResponse(BaseModel):
    id: PyObjectId = Field(alias="_id") 
    location: str
    start_date: date
    end_date: date
    temperatures: List[DailyTemperature]
    created_at: datetime

class WeatherUpdateRequest(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def check_date_range(self) -> 'WeatherUpdateRequest':
        if self.start_date > self.end_date:
            raise ValueError('A nova data inicial não pode ser posterior à data final.')
        return self