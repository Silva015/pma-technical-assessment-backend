from fastapi import FastAPI
from app.routers import weather, export

app = FastAPI(title="Weather API")

@app.get("/")
async def root():
    return {"message": "API está no ar!"}

app.include_router(weather.router)
app.include_router(export.router)