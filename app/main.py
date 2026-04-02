from fastapi import FastAPI
from app.routers import weather

app = FastAPI(title="Weather API")


@app.get("/")
async def root():
    return {"message": "API está no ar!"}

app.include_router(weather.router)