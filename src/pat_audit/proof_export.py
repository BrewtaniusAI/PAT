from __future__ import annotations
import json
from pathlib import Path
from pat_audit.receipts import generate_receipt

def export_proof_bundle(path: str | Path, out_path: str | Path | None = None) -> Path:
    source = Path(path)
    bundle = {
        "kind": "pat_proof_bundle",
        "receipt": generate_receipt(source),
        "artifacts": [
            {
                "path": source.name,
                "role": "primary_artifact"
            }
        ],
        "notes": [
            "Bundle prepared for Proof Vault or DOI-linked archival flow."
        ]
    }
    target = Path(out_path) if out_path else source.with_suffix(source.suffix + ".proof.json")
    target.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    return target
