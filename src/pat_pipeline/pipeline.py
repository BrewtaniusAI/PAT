from pat_core.dialect import detect_dialect
from pat_core.language_profiles import load_profile
from pat_core.phoneme import to_phonemes
from pat_core.tokenizer import tokenize_with_profile
from pat_policy.policy import enforce_policy
from pat_validation.validator import validate_input

SCHEMA_VERSION = "0.1"

def run_pipeline(input_text: str, profile_code: str | None = None) -> dict:
    validate_input(input_text)
    policy_result = enforce_policy(input_text)
    profile = load_profile(profile_code)
    tokens = tokenize_with_profile(input_text, profile)
    dialect = detect_dialect(input_text, profile)
    phonemes = to_phonemes(tokens)

    return {
        "schema_version": SCHEMA_VERSION,
        "input": input_text,
        "status": "processed",
        "tokens": tokens,
        "phonemes": phonemes,
        "dialect": {
            "label": dialect.label,
            "confidence": dialect.confidence,
            "matches": dialect.matches,
        },
        "policy": {
            "passed": policy_result.passed,
            "flags": policy_result.flags,
        },
        "profile_code": profile_code,
    }
