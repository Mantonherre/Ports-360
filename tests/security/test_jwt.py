import os
import subprocess
import time

import httpx
import pytest
from asgi_lifespan import LifespanManager
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from libs.auth_middleware import get_password_token


def _docker_available() -> bool:
    """Return True if both docker and docker-compose are available."""
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
def keycloak_container():
    subprocess.run(["docker-compose", "up", "-d", "keycloak"], check=True)
    # wait for Keycloak
    time.sleep(10)
    yield
    subprocess.run(["docker-compose", "down"], check=True)


@pytest.mark.asyncio
async def test_jwt_required(keycloak_container):
    os.environ["KEYCLOAK_URL"] = "http://localhost:8181"
    os.environ["KEYCLOAK_REALM"] = "smartport"
    token = get_password_token("dashboard", "admin", "admin")
    from services.context_adapter.app.main import app

    sample = {
        "id": "sensor:jwt",
        "type": "temperature",
        "location": {"type": "Point", "coordinates": [0, 0]},
        "measuredProperty": "temperature",
        "unit": "C",
        "lastValue": 1.0,
    }

    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app), base_url="http://test"
        ) as client:
            resp = await client.post(
                "/events/ingest",
                json=[sample],
                headers={"Authorization": f"Bearer {token}"},
            )
            assert resp.status_code == 202
            resp2 = await client.post("/events/ingest", json=[sample])
            assert resp2.status_code == 401
