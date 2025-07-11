import asyncio
import json
import os
import subprocess
import time
import shutil

import pytest

import asyncpg
from asgi_lifespan import LifespanManager
from asyncio_mqtt import Client


def _docker_available() -> bool:
    """Return True if docker and docker-compose are available."""
    try:
        subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        subprocess.run(
            ["docker-compose", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except Exception:
        return False


if not _docker_available():
    pytest.skip("docker not available", allow_module_level=True)


@pytest.fixture(scope="module")
def services():
    subprocess.run(["docker-compose", "up", "-d", "postgres", "mosquitto"], check=True)
    time.sleep(5)
    yield
    subprocess.run(["docker-compose", "down"], check=True)


@pytest.mark.asyncio
async def test_insert(services):
    os.environ["PGHOST"] = "localhost"
    os.environ["PGUSER"] = "postgres"
    os.environ["PGPASSWORD"] = "smartport"
    os.environ["PGDATABASE"] = "postgres"
    os.environ["MQTT_HOST"] = "localhost"
    os.environ["MQTT_PORT"] = "1883"

    subprocess.run(
        ["alembic", "upgrade", "head"], cwd="services/timeseries", check=True
    )

    from services.timeseries.app.main import app

    async with LifespanManager(app):
        async with Client("localhost", 1883) as pub:
            for i in range(5):
                payload = {
                    "id": f"sensor:{i}",
                    "type": "temperature",
                    "location": {"type": "Point", "coordinates": [0, 0]},
                    "measuredProperty": "temperature",
                    "unit": "C",
                    "lastValue": float(i),
                }
                await pub.publish(
                    f"smartport/Sensor/{payload['id']}", json.dumps(payload)
                )
            await asyncio.sleep(2)

    conn = await asyncpg.connect(
        host="localhost", user="postgres", password="smartport", database="postgres"
    )
    count = await conn.fetchval("SELECT count(*) FROM sensor_snapshot")
    await conn.close()
    assert count == 5
