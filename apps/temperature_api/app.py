from fastapi import FastAPI, Query
from typing import Optional
import random
import os
from datetime import datetime

app = FastAPI(title="Temperature API", version="0.1.0")


def build_response(location: str):
    return {
        "value": round(random.uniform(18.0, 28.0), 1),
        "unit": "°C",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": location,
        "status": "ok",
        "sensor_type": "temperature",
    }


@app.get("/temperature")
async def temperature_by_location(
    location: Optional[str] = Query("", description="Room name"),
):
    return build_response(location)
