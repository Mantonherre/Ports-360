import json
import os
from typing import List

from prometheus_client import (
    Counter,
    start_http_server,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

from fastapi.responses import Response

from fastapi import FastAPI, HTTPException, Depends
from asyncio_mqtt import Client
from jsonschema import validate, ValidationError

from .schema_cache import get_schema
from libs.auth_middleware import auth_dependency

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

app = FastAPI(title="Context Adapter")

INGEST_REQUESTS_TOTAL = Counter("ingest_requests_total", "Total ingest requests")
MQTT_MESSAGES_TOTAL = Counter("mqtt_messages_total", "MQTT messages published")

mqtt_client = Client(
    MQTT_HOST, MQTT_PORT, username=MQTT_USERNAME or None, password=MQTT_PASSWORD or None
)
cache: dict[str, dict] = {}


@app.on_event("startup")
async def startup():
    start_http_server(8001)
    await mqtt_client.connect()


@app.get("/metrics")
async def metrics() -> Response:
    """Return Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


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
async def ingest(entities: List[dict], _=Depends(auth_dependency)):
    INGEST_REQUESTS_TOTAL.inc()
    for entity in entities:
        entity_type = detect_type(entity)
        try:
            validate(instance=entity, schema=get_schema(entity_type))
        except ValidationError as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        topic = f"smartport/{entity_type}/{entity['id']}"
        payload = json.dumps(entity)
        await mqtt_client.publish(topic, payload)
        MQTT_MESSAGES_TOTAL.inc()
        cache[(entity_type, entity["id"])] = entity
    return {"status": "accepted"}


@app.get("/entities/{type}/{id}")
async def get_entity(type: str, id: str, _=Depends(auth_dependency)):
    entity = cache.get((type, id))
    if not entity:
        raise HTTPException(status_code=404)
    return entity


@app.patch("/entities/{type}/{id}", status_code=202)
async def patch_entity(type: str, id: str, patch: dict, _=Depends(auth_dependency)):
    if not isinstance(patch, dict):
        raise HTTPException(status_code=400, detail="invalid patch")
    topic = f"smartport/{type}/{id}"
    payload = json.dumps(patch)
    await mqtt_client.publish(topic, payload)
    MQTT_MESSAGES_TOTAL.inc()
    # merge into cache if exists
    if (type, id) in cache:
        cache[(type, id)].update(patch)
    else:
        cache[(type, id)] = patch
    return {"status": "accepted"}
