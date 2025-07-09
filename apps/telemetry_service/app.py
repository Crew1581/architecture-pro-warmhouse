from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
import random

app = FastAPI(title="Telemetry Service", version="0.1.0")

_DATA: dict[str, list] = {}

class TelemetrySample(BaseModel):
    device_id: str
    ts: datetime
    value: float
    unit: str


@app.post("/telemetry", status_code=202)
async def ingest(sample: TelemetrySample):
    _DATA.setdefault(sample.device_id, []).append(sample)
    return {"status": "accepted"}


@app.get("/devices/{device_id}/telemetry", response_model=List[TelemetrySample])
async def history(device_id: str):
    return _DATA.get(device_id, []) 