from fastapi import FastAPI
from app.routers import weather, export

description = """
**Welcome to the Weather & Tourism API!** 🌍☀️

This API was developed as part of a Technical Assessment and provides a complete system for managing weather data with third-party integrations.

### Key Features:
* **Weather CRUD:** Create, read, update, and delete temperature histories for any location.
* **Intelligent Validation:** The system validates date ranges and verifies location existence via geocoding.
* **API Integrations:** Each search automatically generates:
  * 📍 An exact **Google Maps** link.
  * 📖 A clean historical/cultural summary from **Wikipedia**.
  * 🎥 Tourism search links for **YouTube**.
* **Data Export:** Download the entire database in `JSON`, `CSV`, or `Markdown` formats.
"""

app = FastAPI(
    title="Weather & Tourism API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Arthur Silva Carneiro",
        "url": "https://www.linkedin.com/in/arthur-carneiro-7b0538234/",
    }
)

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "API is up and running!"}

app.include_router(weather.router)
app.include_router(export.router)