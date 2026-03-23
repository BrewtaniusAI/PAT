from __future__ import annotations
import re
import unicodedata

DEFAULT_PATTERN = re.compile(r"\b[\w'-]+\b", re.UNICODE)

def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text)

def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    return [m.group(0).lower() for m in DEFAULT_PATTERN.finditer(normalized)]

def tokenize_with_profile(text: str, profile: dict | None) -> list[str]:
    # Current implementation preserves Unicode and uses the base tokenizer.
    # Profile-specific character handling can deepen later without breaking contract.
    _ = profile
    return tokenize(text)
