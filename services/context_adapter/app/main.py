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

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from asyncio_mqtt import Client, MqttError
import asyncio
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

mqtt_client: Client | None = None
cache: dict[str, dict] = {}

ws_clients: set[WebSocket] = set()


async def broadcast(message: str) -> None:
    """Send a message to all connected WebSocket clients."""
    for ws in list(ws_clients):
        try:
            await ws.send_text(message)
        except Exception:
            ws_clients.discard(ws)


async def mqtt_worker() -> None:
    async with mqtt_client.filtered_messages("smartport/#") as messages:
        await mqtt_client.subscribe("smartport/#")
        async for msg in messages:
            await broadcast(msg.payload.decode())


@app.on_event("startup")
async def startup():
    start_http_server(8001)
    global mqtt_client
    mqtt_client = Client(
        MQTT_HOST,
        MQTT_PORT,
        username=MQTT_USERNAME or None,
        password=MQTT_PASSWORD or None,
    )
    while True:
        try:
            await mqtt_client.connect()
            break
        except MqttError as exc:
            print(f"MQTT connection failed: {exc}. Retrying in 5s")
            await asyncio.sleep(5)
    app.mqtt_task = asyncio.create_task(mqtt_worker())


@app.get("/metrics")
async def metrics() -> Response:
    """Return Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.on_event("shutdown")
async def shutdown():
    app.mqtt_task.cancel()
    await asyncio.gather(app.mqtt_task, return_exceptions=True)
    if mqtt_client is not None:
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients.discard(websocket)


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
