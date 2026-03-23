from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationConfig:
    min_length: int = 1
    max_length: int = 5000

def validate_input(text: str, config: ValidationConfig | None = None) -> bool:
    cfg = config or ValidationConfig()
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    normalized = text.strip()
    if len(normalized) < cfg.min_length:
        raise ValueError("Input cannot be empty.")
    if len(text) > cfg.max_length:
        raise ValueError(f"Input exceeds max length of {cfg.max_length}.")
    return True
