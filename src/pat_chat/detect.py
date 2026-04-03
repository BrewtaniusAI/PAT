"""Auto-detect language from text across all 71 African language profiles.

Supports both single-language detection and code-switching detection
(identifying multiple languages mixed within a single text).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from pat_core.dialect import DialectResult, detect_dialect
from pat_core.language_profiles import list_profiles, load_profile


@dataclass(frozen=True)
class DetectionResult:
    """Result of scanning text against all language profiles."""

    code: str
    name: str
    confidence: float
    matches: list[str]


@dataclass(frozen=True)
class CodeSwitchResult:
    """Result of code-switching detection — multiple languages in one text.

    Attributes:
        primary: The dominant language detected.
        secondary: Other languages detected above the confidence threshold.
        is_code_switched: True if multiple languages are detected.
    """

    primary: DetectionResult
    secondary: list[DetectionResult]
    is_code_switched: bool


@lru_cache(maxsize=1)
def _load_all_profiles() -> tuple[tuple[str, dict], ...]:
    """Load and cache all language profiles to avoid repeated disk I/O."""
    profiles = []
    for code in list_profiles():
        profile = load_profile(code)
        if profile is not None:
            profiles.append((code, profile))
    return tuple(profiles)


def detect_language(text: str) -> DetectionResult:
    """Scan input text against every profile and return the best match.

    Returns a DetectionResult with code="unknown" if no profile matches.
    """
    best_code = "unknown"
    best_name = "Unknown"
    best_confidence = 0.0
    best_matches: list[str] = []

    for code, profile in _load_all_profiles():
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


def detect_code_switching(
    text: str, threshold: float = 0.4
) -> CodeSwitchResult:
    """Detect multiple languages in a single text (code-switching).

    Code-switching is the fluid mixing of multiple languages within a single
    utterance — common across urban African populations (e.g., isiZulu + English,
    French + Wolof). This function identifies all languages present above the
    confidence threshold, enabling PAT to handle real-world multilingual input.

    Args:
        text: The input text to analyze.
        threshold: Minimum confidence for a language to be considered present.

    Returns:
        CodeSwitchResult with primary language and any secondary languages.
    """
    scored: list[DetectionResult] = []

    for code, profile in _load_all_profiles():
        result: DialectResult = detect_dialect(text, profile)
        if result.confidence >= threshold:
            scored.append(
                DetectionResult(
                    code=code,
                    name=profile.get("name", code),
                    confidence=result.confidence,
                    matches=result.matches,
                )
            )

    # Sort by confidence descending
    scored.sort(key=lambda r: r.confidence, reverse=True)

    if not scored:
        unknown = DetectionResult(
            code="unknown", name="Unknown", confidence=0.0, matches=[]
        )
        return CodeSwitchResult(primary=unknown, secondary=[], is_code_switched=False)

    primary = scored[0]
    secondary = scored[1:]

    return CodeSwitchResult(
        primary=primary,
        secondary=secondary,
        is_code_switched=len(scored) > 1,
    )
