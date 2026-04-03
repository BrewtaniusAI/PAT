from __future__ import annotations
from pathlib import Path
from pat_builder.builder import build_dataset

def build_dataset_batch(input_dir: str | Path, output_dir: str | Path) -> dict:
    src = Path(input_dir)
    dst = Path(output_dir)
    dst.mkdir(parents=True, exist_ok=True)

    built = []
    skipped = []

    for path in sorted(src.glob("*.json")):
        out_path = dst / path.name
        try:
            build_dataset(path, out_path)
            built.append(str(out_path))
        except Exception:
            skipped.append(str(path))

    return {
        "built": built,
        "skipped": skipped,
        "count_built": len(built),
        "count_skipped": len(skipped),
    }
