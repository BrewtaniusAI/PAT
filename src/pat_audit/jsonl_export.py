from __future__ import annotations
import json
from pathlib import Path

def append_jsonl(path: str | Path, record: dict) -> Path:
    p = Path(path)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return p
