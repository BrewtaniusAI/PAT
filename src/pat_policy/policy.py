from dataclasses import dataclass

FORBIDDEN_PATTERNS = (
    "impersonate",
    "political manipulation",
    "fake message",
)

@dataclass(frozen=True)
class PolicyResult:
    passed: bool
    flags: list[str]

def evaluate_policy(text: str) -> PolicyResult:
    lowered = text.lower()
    flags = [pattern for pattern in FORBIDDEN_PATTERNS if pattern in lowered]
    return PolicyResult(passed=len(flags) == 0, flags=flags)

def enforce_policy(text: str) -> PolicyResult:
    result = evaluate_policy(text)
    if not result.passed:
        raise PermissionError(f"Policy violation detected: {', '.join(result.flags)}")
    return result
