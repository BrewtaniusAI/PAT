"""Language-aware system prompts for PAT chat."""
from __future__ import annotations

from pat_core.language_profiles import list_profiles, load_profile


def build_system_prompt(language_code: str | None, language_name: str | None) -> str:
    """Build a system prompt that instructs the LLM to respond in the given language."""
    all_codes = list_profiles()
    language_list = []
    for code in all_codes:
        profile = load_profile(code)
        if profile:
            language_list.append(f"{profile['name']} ({code})")

    base = (
        "You are PAT — a Pan-African Language AI assistant. "
        "You help users communicate in African languages. "
        "You are knowledgeable about African languages, cultures, and linguistics.\n\n"
        f"You support {len(all_codes)} African languages: {', '.join(language_list)}.\n\n"
    )

    if language_code and language_name:
        base += (
            f"The user is communicating in **{language_name}** (code: {language_code}). "
            f"Respond primarily in {language_name}. "
            f"You may include brief English translations in parentheses when using "
            f"complex or uncommon terms to aid understanding.\n\n"
        )
    else:
        base += (
            "The user's language has not been identified yet. "
            "Try to detect what language they are using from context. "
            "If you can identify the language, respond in that language. "
            "Otherwise, respond in English and ask which African language "
            "they would like to communicate in.\n\n"
        )

    base += (
        "Guidelines:\n"
        "- Preserve all diacritics, tone marks, and special characters\n"
        "- Be culturally respectful and contextually aware\n"
        "- If asked about a language you support, share relevant linguistic insights\n"
        "- You can switch languages mid-conversation if the user does\n"
        "- Always be helpful, accurate, and respectful of African linguistic heritage\n"
    )

    return base
