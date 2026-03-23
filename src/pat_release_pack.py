from __future__ import annotations
import json
from pathlib import Path
from pat_release import check_release_readiness
from pat_version import get_version

def generate_release_summary(repo_root: str | Path = ".") -> dict:
    root = Path(repo_root)
    status = check_release_readiness(root)
    return {
        "name": "PAT",
        "version": get_version(),
        "ready": status["ready"],
        "missing": status["missing"],
        "manifest_path": str(root / "release_manifest.json"),
        "publication_docs": [
            "docs/GITHUB_RELEASE_TEXT.md",
            "docs/ZENODO_PUBLICATION_TEXT.md",
            "docs/PUBLICATION_CHECKLIST.md",
        ],
    }
