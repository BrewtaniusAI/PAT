from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass

@dataclass(frozen=True)
class DialectResult:
    label: str
    confidence: float
    matches: list[str]


def _is_word_boundary_safe(keyword: str) -> bool:
    """Check if a keyword can safely use \\b word boundaries.

    Keywords containing Unicode combining marks (category Mn) break \\b
    because Python's regex treats combining marks as non-word characters.
    """
    return all(unicodedata.category(ch) != 'Mn' for ch in keyword)


def _keyword_matches(keyword: str, text: str) -> bool:
    """Match a keyword in text, using word boundaries when safe.

    Single/two-character keywords act as character-presence indicators
    (e.g., Yorùbá ẹ, ọ, ṣ) and use substring matching so they detect
    the character inside words like "orúkọ" or "káàárọ̀".
    """
    kw = keyword.lower()
    if len(kw) <= 2:
        return kw in text
    if _is_word_boundary_safe(kw):
        return re.search(r'\b' + re.escape(kw) + r'\b', text) is not None
    # Fallback: match with surrounding whitespace/punctuation/boundaries
    return re.search(r'(?<!\w)' + re.escape(kw) + r'(?!\w)', text) is not None


def detect_dialect(text: str, profile: dict | None = None) -> DialectResult:
    lowered = text.lower()
    if profile:
        keywords = profile.get("keywords", [])
        matches = [kw for kw in keywords if _keyword_matches(kw, lowered)]
        if matches:
            confidence = min(1.0, 0.4 + 0.1 * len(matches))
            return DialectResult(label=profile.get("code", "unknown"), confidence=confidence, matches=matches)
    return DialectResult(label="unknown", confidence=0.0, matches=[])
