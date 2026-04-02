from __future__ import annotations
import json
from pathlib import Path

PROFILE_DIR = Path(__file__).resolve().parents[2] / "configs" / "language_profiles"

def list_profiles() -> list[str]:
    return sorted(p.stem for p in PROFILE_DIR.glob("*.json"))

def load_profile(profile_code: str | None) -> dict | None:
    if not profile_code:
        return None
    # Reject path traversal attempts
    if "/" in profile_code or "\\" in profile_code or ".." in profile_code:
        raise ValueError(f"Invalid profile code: {profile_code}")
    path = (PROFILE_DIR / f"{profile_code}.json").resolve()
    if not str(path).startswith(str(PROFILE_DIR.resolve())):
        raise ValueError(f"Invalid profile code: {profile_code}")
    if not path.exists():
        raise ValueError(f"Unknown profile: {profile_code}")
    return json.loads(path.read_text(encoding="utf-8"))
