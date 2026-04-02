"""Auto-detect language from text across all 71 African language profiles."""
from __future__ import annotations

from dataclasses import dataclass

from pat_core.dialect import DialectResult, detect_dialect
from pat_core.language_profiles import list_profiles, load_profile


@dataclass(frozen=True)
class DetectionResult:
    """Result of scanning text against all language profiles."""

    code: str
    name: str
    confidence: float
    matches: list[str]


def detect_language(text: str) -> DetectionResult:
    """Scan input text against every profile and return the best match.

    Returns a DetectionResult with code="unknown" if no profile matches.
    """
    best_code = "unknown"
    best_name = "Unknown"
    best_confidence = 0.0
    best_matches: list[str] = []

    for code in list_profiles():
        profile = load_profile(code)
        if profile is None:
            continue
        result: DialectResult = detect_dialect(text, profile)
        if result.confidence > best_confidence:
            best_code = code
            best_name = profile.get("name", code)
            best_confidence = result.confidence
            best_matches = result.matches

    return DetectionResult(
        code=best_code,
        name=best_name,
        confidence=best_confidence,
        matches=best_matches,
    )
