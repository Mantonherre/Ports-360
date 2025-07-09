import json
from pathlib import Path

import yaml
from jsonschema import validate

SCHEMA_PATH = Path(__file__).parents[2] / "docs" / "domain" / "ngsi-ld.yaml"
with SCHEMA_PATH.open() as f:
    SCHEMA = yaml.safe_load(f)

ENTITY_NAMES = [
    "PortArea",
    "Sensor",
    "EnergyAsset",
    "Vessel",
    "BathyPoint",
]


def load_example(name: str):
    path = Path(__file__).parent / "examples" / f"{name}.json"
    with path.open() as f:
        return json.load(f)


def test_schema_examples():
    for name in ENTITY_NAMES:
        instance = load_example(name)
        schema = {"$ref": f"#/$defs/{name}", **SCHEMA}
        validate(instance, schema)
