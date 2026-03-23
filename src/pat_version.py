from __future__ import annotations
from pathlib import Path

VERSION_FILE = Path(__file__).resolve().parents[1] / "VERSION"

def get_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()

def bump_patch(version: str) -> str:
    major, minor, patch = version.split(".")
    return f"{major}.{minor}.{int(patch) + 1}"
