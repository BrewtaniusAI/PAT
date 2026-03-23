from __future__ import annotations
import json
from pathlib import Path

def _load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate_pipeline_output_file(output_path: str | Path, schema_path: str | Path) -> dict:
    data = _load_json(output_path)
    schema = _load_json(schema_path)

    required = schema.get("required", [])
    missing = [key for key in required if key not in data]

    if missing:
        return {
            "valid": False,
            "missing": missing,
            "checked_against": str(schema_path),
        }

    return {
        "valid": True,
        "missing": [],
        "checked_against": str(schema_path),
    }
