import asyncio
import json
import os
from datetime import datetime
from time import perf_counter

from prometheus_client import (
    Counter,
    Histogram,
    start_http_server,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from fastapi.responses import Response

from asyncio_mqtt import Client
from fastapi import FastAPI, Depends
from sqlalchemy import insert, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .models import SensorSnapshot, EnergySnapshot, BathySnapshot
from libs.auth_middleware import auth_dependency

PGHOST = os.getenv("PGHOST", "postgres")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "smartport")
PGDATABASE = os.getenv("PGDATABASE", "postgres")
MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

DATABASE_URL = f"postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI(title="Timeseries Writer")

MQTT_MESSAGES_TOTAL = Counter("mqtt_messages_total", "MQTT messages processed")
DB_INSERT_SECONDS = Histogram("db_insert_seconds", "DB insert duration")


def health() -> dict:
    return {"status": "ok"}


@app.get("/health")
async def health_endpoint(_=Depends(auth_dependency)):
    return health()


@app.get("/metrics")
async def metrics() -> Response:
    """Return Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


BUFFER = {"sensor": [], "energy": [], "bathy": []}
LOCK = asyncio.Lock()


async def flush():
    async with LOCK:
        sensor_rows = BUFFER["sensor"]
        energy_rows = BUFFER["energy"]
        bathy_rows = BUFFER["bathy"]
        BUFFER["sensor"] = []
        BUFFER["energy"] = []
        BUFFER["bathy"] = []
    if not (sensor_rows or energy_rows or bathy_rows):
        return
    start = perf_counter()
    async with SessionLocal() as session:
        async with session.begin():
            if sensor_rows:
                await session.execute(
                    insert(SensorSnapshot),
                    [
                        {
                            "id": r["id"],
                            "ts": r.get("ts"),
                            "measuredproperty": r.get("measuredproperty"),
                            "value": r.get("value"),
                            "geom": func.ST_SetSRID(
                                func.ST_MakePoint(r["lon"], r["lat"]), 4326
                            ),
                        }
                        for r in sensor_rows
                    ],
                )
            if energy_rows:
                await session.execute(
                    insert(EnergySnapshot),
                    [
                        {
                            "id": r["id"],
                            "ts": r.get("ts"),
                            "soc": r.get("soc"),
                            "power_kw": r.get("power_kw"),
                        }
                        for r in energy_rows
                    ],
                )
            if bathy_rows:
                await session.execute(
                    insert(BathySnapshot),
                    [
                        {
                            "id": r["id"],
                            "ts": r.get("ts"),
                            "depth_m": r.get("depth_m"),
                            "geom": func.ST_SetSRID(
                                func.ST_MakePoint(r["lon"], r["lat"]), 4326
                            ),
                        }
                        for r in bathy_rows
                    ],
                )
    DB_INSERT_SECONDS.observe(perf_counter() - start)


async def flush_worker():
    while True:
        await asyncio.sleep(1)
        await flush()


async def mqtt_worker():
    async with Client(MQTT_HOST, MQTT_PORT) as client:
        async with client.filtered_messages("smartport/#") as messages:
            await client.subscribe("smartport/#")
            async for msg in messages:
                parts = msg.topic.split("/")
                if len(parts) < 3:
                    continue
                entity_type = parts[1]
                entity_id = parts[2]
                try:
                    data = json.loads(msg.payload.decode())
                except json.JSONDecodeError:
                    continue
                item = {"id": entity_id}
                if "timestamp" in data:
                    try:
                        item["ts"] = datetime.fromisoformat(data["timestamp"])
                    except Exception:
                        pass
                if entity_type == "Sensor":
                    coords = data.get("location", {}).get("coordinates", [0, 0])
                    item.update(
                        {
                            "measuredproperty": data.get("measuredProperty"),
                            "value": data.get("lastValue"),
                            "lon": coords[0],
                            "lat": coords[1],
                        }
                    )
                    async with LOCK:
                        BUFFER["sensor"].append(item)
                elif entity_type == "EnergyAsset":
                    item.update(
                        {
                            "soc": data.get("state_of_charge") or data.get("soc"),
                            "power_kw": data.get("power_kw") or data.get("capacity_kW"),
                        }
                    )
                    async with LOCK:
                        BUFFER["energy"].append(item)
                elif entity_type == "BathyPoint":
                    coords = data.get("location", {}).get("coordinates", [0, 0])
                    item.update(
                        {
                            "depth_m": data.get("depth_m"),
                            "lon": coords[0],
                            "lat": coords[1],
                        }
                    )
                    async with LOCK:
                        BUFFER["bathy"].append(item)
                MQTT_MESSAGES_TOTAL.inc()
                async with LOCK:
                    total = sum(len(v) for v in BUFFER.values())
                if total >= 100:
                    await flush()


@app.on_event("startup")
async def startup_event():
    start_http_server(8001)
    app.mqtt_task = asyncio.create_task(mqtt_worker())
    app.flush_task = asyncio.create_task(flush_worker())


@app.on_event("shutdown")
async def shutdown_event():
    app.mqtt_task.cancel()
    app.flush_task.cancel()
    await asyncio.gather(app.mqtt_task, app.flush_task, return_exceptions=True)
