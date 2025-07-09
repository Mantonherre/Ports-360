import json
import os
from typing import List

from fastapi import FastAPI, HTTPException
from asyncio_mqtt import Client
from jsonschema import validate, ValidationError

from .schema_cache import get_schema

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

app = FastAPI(title="Context Adapter")

mqtt_client = Client(
    MQTT_HOST, MQTT_PORT, username=MQTT_USERNAME or None, password=MQTT_PASSWORD or None
)
cache: dict[str, dict] = {}


@app.on_event("startup")
async def startup():
    await mqtt_client.connect()


@app.on_event("shutdown")
async def shutdown():
    await mqtt_client.disconnect()


def detect_type(entity: dict) -> str:
    if "depth_m" in entity:
        return "BathyPoint"
    if "capacity_kW" in entity:
        return "EnergyAsset"
    if "lastValue" in entity:
        return "Sensor"
    if "geometry" in entity:
        return "PortArea"
    if "imo" in entity:
        return "Vessel"
    raise ValueError("Unknown entity type")


@app.post("/events/ingest", status_code=202)
async def ingest(entities: List[dict]):
    for entity in entities:
        entity_type = detect_type(entity)
        try:
            validate(instance=entity, schema=get_schema(entity_type))
        except ValidationError as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        topic = f"smartport/{entity_type}/{entity['id']}"
        payload = json.dumps(entity)
        await mqtt_client.publish(topic, payload)
        cache[(entity_type, entity["id"])] = entity
    return {"status": "accepted"}


@app.get("/entities/{type}/{id}")
async def get_entity(type: str, id: str):
    entity = cache.get((type, id))
    if not entity:
        raise HTTPException(status_code=404)
    return entity


@app.patch("/entities/{type}/{id}", status_code=202)
async def patch_entity(type: str, id: str, patch: dict):
    if not isinstance(patch, dict):
        raise HTTPException(status_code=400, detail="invalid patch")
    topic = f"smartport/{type}/{id}"
    payload = json.dumps(patch)
    await mqtt_client.publish(topic, payload)
    # merge into cache if exists
    if (type, id) in cache:
        cache[(type, id)].update(patch)
    else:
        cache[(type, id)] = patch
    return {"status": "accepted"}
