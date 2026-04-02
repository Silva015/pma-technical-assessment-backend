import httpx
from datetime import date
from fastapi import HTTPException
from app.schemas.weather import DailyTemperature

async def fetch_real_weather(location: str, start_date: date, end_date: date):
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=pt"
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()
        if not geo_data.get("results"):
            raise HTTPException(status_code=404, detail=f"A localização '{location}' não foi encontrada no mapa.")

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        official_name = geo_data["results"][0].get("name", location)
        country = geo_data["results"][0].get("country", "")
        
        full_location_name = f"{official_name}, {country}"

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"start_date={start_date}&end_date={end_date}&"
            f"daily=temperature_2m_max&timezone=auto"
        )
        
        weather_response = await client.get(weather_url)
        if weather_response.status_code != 200:
            raise HTTPException(
                status_code=400, 
                detail="Erro ao buscar o clima. Verifique se as datas não estão muito no futuro (limite de 14 dias para previsão)."
            )
            
        weather_data = weather_response.json()

        temperatures = []
        daily = weather_data.get("daily", {})
        dates = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])

        for i in range(len(dates)):
            temperatures.append(
                DailyTemperature(
                    date=dates[i],
                    temp_celsius=max_temps[i],
                    description="Temperatura Máxima Diária"
                )
            )

        return full_location_name, lat, lon, temperatures