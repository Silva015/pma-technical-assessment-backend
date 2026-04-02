from fastapi import FastAPI

app = FastAPI(title="Weather API")

@app.get("/")
async def root():
    return {"message": "API está no ar!"}