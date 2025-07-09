import asyncio
import json
import os
import subprocess
import time
from pathlib import Path

import pytest
from asyncio_mqtt import Client
from jsonschema import validate
import yaml

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "docs" / "domain" / "ngsi-ld.yaml"
with SCHEMA_PATH.open() as f:
    SCHEMA = yaml.safe_load(f)


def load_schema(entity_type: str) -> dict:
    return {"$ref": f"#/$defs/{entity_type}", **SCHEMA}


@pytest.fixture(scope="module")
def mqtt_broker():
    proc = subprocess.Popen(["mosquitto", "-p", "1884"])
    time.sleep(1)
    yield
    proc.terminate()
    proc.wait()


@pytest.mark.asyncio
async def test_publish(tmp_path, mqtt_broker):
    os.environ["MQTT_HOST"] = "localhost"
    os.environ["MQTT_PORT"] = "1884"
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text((Path("tools/sensor_sim/config.yaml").read_text()))

    proc = subprocess.Popen(
        [
            "python",
            "tools/sensor_sim/sensor_sim.py",
            "--config",
            str(cfg),
            "--rate",
            "0.5",
            "--duration",
            "2",
            "--mqtt-host",
            "localhost",
            "--mqtt-port",
            "1884",
        ]
    )
    await asyncio.sleep(0.1)
    async with Client("localhost", 1884) as sub:
        async with sub.filtered_messages("smartport/#") as messages:
            await sub.subscribe("smartport/#")
            msg = await asyncio.wait_for(messages.__anext__(), timeout=5)
    proc.wait()
    data = json.loads(msg.payload.decode())
    t = msg.topic.split("/")[1]
    validate(data, load_schema(t))
