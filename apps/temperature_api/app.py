from fastapi import FastAPI, Query
from typing import Optional
import random
import os
from datetime import datetime

app = FastAPI(title="Temperature API", version="0.1.0")

SENSOR_MAP = {
    "1": "Living Room",
    "2": "Bedroom",
    "3": "Kitchen",
}


def build_response(sensor_id: str, location: str):
    return {
        "value": round(random.uniform(18.0, 28.0), 1),
        "unit": "°C",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": location,
        "status": "ok",
        "sensor_id": sensor_id,
        "sensor_type": "temperature",
    }


@app.get("/temperature")
async def temperature_by_location(
    location: Optional[str] = Query("", description="Room name"),
    sensorId: Optional[str] = Query("", alias="sensorId", description="Sensor ID"),
):
    loc = location
    sid = sensorId

    if not loc:
        loc = SENSOR_MAP.get(sid, "Unknown")
    if not sid:
        sid = {v: k for k, v in SENSOR_MAP.items()}.get(loc, "0")

    return build_response(sid, loc)
