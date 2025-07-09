import asyncio
import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path

import click
import yaml
from asyncio_mqtt import Client
from jsonschema import validate, ValidationError

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "docs" / "domain" / "ngsi-ld.yaml"


def load_schema(entity_type: str) -> dict:
    with SCHEMA_PATH.open() as f:
        schema = yaml.safe_load(f)
    return {"$ref": f"#/$defs/{entity_type}", **schema}


def load_config(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def make_sensor(cfg: dict) -> dict:
    return {
        "id": cfg["id"],
        "type": cfg.get("sensor_type", "sensor"),
        "location": {"type": "Point", "coordinates": cfg.get("location", [0, 0])},
        "measuredProperty": cfg.get("measuredProperty", cfg.get("sensor_type", "temp")),
        "unit": cfg.get("unit", "C"),
        "lastValue": random.random() * 100,
    }


def make_energy(cfg: dict) -> dict:
    return {
        "id": cfg["id"],
        "kind": cfg.get("kind", "battery"),
        "capacity_kW": cfg.get("capacity_kW", 100),
        "state_of_charge": random.random(),
    }


def make_bathy(cfg: dict) -> dict:
    depth = cfg.get("depth_m", 10) + random.uniform(-1, 1)
    return {
        "id": cfg["id"],
        "location": {"type": "Point", "coordinates": cfg.get("location", [0, 0])},
        "depth_m": depth,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


CREATORS = {
    "Sensor": make_sensor,
    "EnergyAsset": make_energy,
    "BathyPoint": make_bathy,
}


async def publish_loop(client: Client, cfg: dict, rate: float):
    entity_type = cfg["entity_type"]
    schema = load_schema(entity_type)
    creator = CREATORS[entity_type]
    while True:
        entity = creator(cfg)
        try:
            validate(instance=entity, schema=schema)
        except ValidationError as ex:
            click.echo(f"Validation error for {entity['id']}: {ex}", err=True)
        else:
            topic = f"smartport/{entity_type}/{entity['id']}"
            await client.publish(topic, json.dumps(entity))
        await asyncio.sleep(rate)


async def run(
    config_path: str,
    mqtt_host: str,
    mqtt_port: int,
    rate: float,
    duration: float | None,
):
    config = load_config(Path(config_path))
    rate = rate or config.get("rate", 1)
    tasks = []
    async with Client(mqtt_host, mqtt_port) as client:
        for cfg in config.get("entities", []):
            tasks.append(asyncio.create_task(publish_loop(client, cfg, rate)))
        if duration:
            await asyncio.sleep(duration)
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
        else:
            await asyncio.gather(*tasks)


@click.command()
@click.option("--config", default="config.yaml", help="YAML config file")
@click.option("--mqtt-host", default=lambda: os.getenv("MQTT_HOST", "mqtt"))
@click.option(
    "--mqtt-port",
    default=lambda: int(os.getenv("MQTT_PORT", "1883")),
    type=int,
)
@click.option("--rate", default=1.0, type=float, help="Publish interval in seconds")
@click.option("--duration", default=None, type=float, help="Run for N seconds and exit")
def main(config, mqtt_host, mqtt_port, rate, duration):
    """Publish fake sensor data to MQTT."""
    asyncio.run(run(config, mqtt_host, mqtt_port, rate, duration))


if __name__ == "__main__":
    main()
