from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DialectResult:
    label: str
    confidence: float
    matches: list[str]

def detect_dialect(text: str, profile: dict | None = None) -> DialectResult:
    lowered = text.lower()
    if profile:
        keywords = profile.get("keywords", [])
        matches = [kw for kw in keywords if kw.lower() in lowered]
        if matches:
            confidence = min(1.0, 0.4 + 0.1 * len(matches))
            return DialectResult(label=profile.get("code", "unknown"), confidence=confidence, matches=matches)
    return DialectResult(label="unknown", confidence=0.0, matches=[])
