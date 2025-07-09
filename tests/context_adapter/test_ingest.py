import asyncio
import json
import os
import subprocess
import time

import pytest
import httpx
from asgi_lifespan import LifespanManager
from asyncio_mqtt import Client


@pytest.fixture(scope="module")
def mqtt_broker():
    proc = subprocess.Popen(["mosquitto", "-p", "1883"])
    time.sleep(1)
    yield
    proc.terminate()
    proc.wait()


@pytest.mark.asyncio
async def test_ingest(mqtt_broker):
    os.environ["MQTT_HOST"] = "localhost"
    os.environ["MQTT_PORT"] = "1883"

    from services.context_adapter.app.main import app

    sample = {
        "id": "sensor:1",
        "type": "temperature",
        "location": {"type": "Point", "coordinates": [0, 0]},
        "measuredProperty": "temperature",
        "unit": "C",
        "lastValue": 25.5,
    }

    async with LifespanManager(app):
        async with Client("localhost", 1883) as sub:
            async with sub.filtered_messages("smartport/#") as messages:
                await sub.subscribe("smartport/#")
                async with httpx.AsyncClient(
                    transport=httpx.ASGITransport(app), base_url="http://test"
                ) as client:
                    resp = await client.post("/events/ingest", json=[sample])
                    assert resp.status_code == 202
                msg = await asyncio.wait_for(messages.__anext__(), timeout=5)
    assert msg.topic == "smartport/Sensor/sensor:1"
    assert json.loads(msg.payload.decode()) == sample
