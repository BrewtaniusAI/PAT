from __future__ import annotations
import json
from pathlib import Path

RELEASE_FILES = [
    "README.md",
    "LICENSE.md",
    "CITATION.cff",
    "pyproject.toml",
    "VERSION",
    "release_manifest.json",
    "docs/OVERVIEW.md",
    "docs/ARCHITECTURE.md",
    "docs/GOVERNANCE.md",
    "docs/ETHICAL_USE.md",
    "docs/REPRODUCIBILITY.md",
    "docs/CHANGELOG.md",
    "docs/GITHUB_RELEASE_DRAFT.md",
    "docs/ZENODO_RELEASE_NOTES.md",
    "schemas/pipeline_output.schema.json",
]

def check_release_readiness(repo_root: str | Path) -> dict:
    root = Path(repo_root)
    present = []
    missing = []
    for rel in RELEASE_FILES:
        if (root / rel).exists():
            present.append(rel)
        else:
            missing.append(rel)

    manifest_ok = False
    manifest_path = root / "release_manifest.json"
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_ok = bool(data.get("name")) and bool(data.get("version"))
        except Exception:
            manifest_ok = False

    return {
        "ready": len(missing) == 0 and manifest_ok,
        "present": present,
        "missing": missing,
        "manifest_ok": manifest_ok,
    }
