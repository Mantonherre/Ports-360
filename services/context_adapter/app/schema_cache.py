from functools import lru_cache
from pathlib import Path
import yaml

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "docs" / "domain" / "ngsi-ld.yaml"


@lru_cache
def load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return yaml.safe_load(f)


@lru_cache
def get_schema(entity_type: str) -> dict:
    base = load_schema()
    return {"$ref": f"#/$defs/{entity_type}", **base}
