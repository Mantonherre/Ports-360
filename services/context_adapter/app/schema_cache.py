from functools import lru_cache
from pathlib import Path
import yaml

# Locate the NGSI-LD schema file by walking up parent directories
_file = Path(__file__).resolve()
for parent in [_file.parent, *_file.parents]:
    candidate = parent / "docs" / "domain" / "ngsi-ld.yaml"
    if candidate.exists():
        SCHEMA_PATH = candidate
        break
else:  # pragma: no cover - executed only if file is missing
    raise FileNotFoundError("ngsi-ld.yaml not found")


@lru_cache
def load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return yaml.safe_load(f)


@lru_cache
def get_schema(entity_type: str) -> dict:
    base = load_schema()
    return {"$ref": f"#/$defs/{entity_type}", **base}
