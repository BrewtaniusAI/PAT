from __future__ import annotations
import json
from pathlib import Path

def build_dataset(input_path: str | Path, output_path: str | Path) -> Path:
    src = Path(input_path)
    dst = Path(output_path)
    data = json.loads(src.read_text(encoding="utf-8"))
    dst.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return dst
