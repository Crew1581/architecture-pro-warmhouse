import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg

app = FastAPI(title="Devices Service", version="0.1.0")

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:postgres@postgres:5432/smarthome")


class DeviceCreate(BaseModel):
    name: str
    type: str
    location: str
    unit: str = "°C"


class Device(DeviceCreate):
    id: int
    value: float | None = None
    status: str | None = None


@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)


@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()


@app.get("/devices", response_model=List[Device])
async def list_devices():
    rows = await app.state.pool.fetch("SELECT * FROM sensors ORDER BY id")
    return [Device(**dict(r)) for r in rows]


@app.post("/devices", response_model=Device, status_code=201)
async def create_device(device: DeviceCreate):
    row = await app.state.pool.fetchrow(
        """
        INSERT INTO sensors (name, type, location, unit, status)
        VALUES ($1,$2,$3,$4,'inactive')
        RETURNING *
        """,
        device.name,
        device.type,
        device.location,
        device.unit,
    )
    return Device(**dict(row))


@app.patch("/devices/{device_id}/state", response_model=Device)
async def update_state(device_id: int, status: str):
    row = await app.state.pool.fetchrow(
        """
        UPDATE sensors SET status=$1, last_updated=NOW() WHERE id=$2 RETURNING *
        """,
        status,
        device_id,
    )
    if not row:
        raise HTTPException(status_code=404, detail="Device not found")
    return Device(**dict(row)) 