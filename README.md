# PMA Technical Assessment Backend

This project is a FastAPI-based backend for the PMA Technical Assessment.

## Setup

1.  **Create a virtual environment:**

    ```bash
    uv venv
    ```

2.  **Activate the virtual environment:**

    ```bash
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

```bash
uv run uvicorn app.main:app --reload
```

The server will be available at `http://localhost:8000`.

## API Documentation

Interactive API documentation (Swagger UI) is available at:
`http://localhost:8000/docs`

# Project Structure

pma-technical-assessment-backend/
├── app/
│ ├── **init**.py
│ ├── main.py # Entry point (starts the app and includes the routers)
│ ├── dependencies.py # Dependency injection (ex: get_db function for MongoDB)
│ ├── core/  
│ │ ├── config.py # Reads .env, centralizes API keys and URLs
│ │ └── database.py # Initializes the MongoDB Atlas engine
│ ├── routers/ # The official FastAPI "Controllers"
│ │ ├── weather.py # CRUD endpoints (POST, GET, PUT, DELETE for weather)
│ │ └── export.py # Endpoints to download JSON, CSV, Markdown, etc.
│ ├── schemas/ # Your "DTOs"
│ │ └── weather.py # Pydantic models (validation of dates, location, etc.)
│ └── services/ # Heavy and isolated logic
│ ├── openweather.py # Functions that call the weather API using httpx
│ └── integrations.py # Functions to call YouTube and Google Maps
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
└── uv.lock
