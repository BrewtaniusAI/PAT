from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: str | Path) -> str:
    file_path = Path(path)
    h = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def generate_receipt(path: str | Path, source: str = "PAT pipeline", schema_version: str = "0.1") -> dict:
    file_path = Path(path)
    return {
        "file": file_path.name,
        "sha256": sha256_file(file_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "schema_version": schema_version,
        "source": source,
    }

def write_receipt(path: str | Path, receipt_path: str | Path | None = None) -> Path:
    file_path = Path(path)
    out = Path(receipt_path) if receipt_path else file_path.with_suffix(file_path.suffix + ".receipt.json")
    out.write_text(json.dumps(generate_receipt(file_path), indent=2), encoding="utf-8")
    return out
