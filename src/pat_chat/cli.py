"""PAT Chat CLI — interactive multilingual chat in the terminal."""
from __future__ import annotations

import sys

from pat_chat.backends import (
    AnthropicBackend,
    ChatBackend,
    EchoBackend,
    OllamaBackend,
    OpenAIBackend,
    auto_select_backend,
)
from pat_chat.engine import ChatEngine
from pat_core.language_profiles import list_profiles, load_profile


def _resolve_backend(backend_name: str | None) -> ChatBackend:
    """Resolve a backend by name, or auto-select."""
    if not backend_name:
        return auto_select_backend()
    name = backend_name.lower()
    if name == "ollama":
        return OllamaBackend()
    if name == "openai":
        return OpenAIBackend()
    if name == "anthropic":
        return AnthropicBackend()
    if name == "echo":
        return EchoBackend()
    print(f"Unknown backend: {backend_name}. Using auto-select.")
    return auto_select_backend()


def _print_banner(engine: ChatEngine) -> None:
    """Print the welcome banner."""
    status = engine.status()
    print()
    print("=" * 60)
    print("  PAT Chat — Pan-African Language AI")
    print("=" * 60)
    print(f"  Backend : {status['backend']}")
    print(f"  Available: {status['backend_available']}")
    if engine.language_code:
        print(f"  Language : {engine.language_name} ({engine.language_code})")
    else:
        print("  Language : Auto-detect")
    print()
    print("  Commands:")
    print("    /quit        — exit chat")
    print("    /reset       — clear history")
    print("    /lang <code> — switch language (e.g. /lang yo)")
    print("    /langs       — list all supported languages")
    print("    /status      — show engine status")
    print("    /help        — show this help")
    print("=" * 60)
    print()


def _handle_command(engine: ChatEngine, command: str) -> bool:
    """Handle a slash command. Returns True if the REPL should continue."""
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0].lower()

    if cmd in ("/quit", "/exit", "/q"):
        print("\nBye!")
        return False

    if cmd == "/reset":
        engine.reset()
        print("Conversation cleared.")
        return True

    if cmd == "/lang":
        if len(parts) < 2:
            print("Usage: /lang <code>  (e.g. /lang yo)")
            return True
        code = parts[1].strip()
        try:
            profile = load_profile(code)
            if profile:
                engine.set_language(code, profile["name"])
                print(f"Switched to {profile['name']} ({code})")
            else:
                print(f"Unknown language code: {code}")
        except ValueError:
            print(f"Unknown language code: {code}")
        return True

    if cmd == "/langs":
        codes = list_profiles()
        print(f"\nSupported languages ({len(codes)}):\n")
        for code in codes:
            profile = load_profile(code)
            name = profile["name"] if profile else code
            print(f"  {code:8s} {name}")
        print()
        return True

    if cmd == "/status":
        status = engine.status()
        for key, value in status.items():
            print(f"  {key}: {value}")
        return True

    if cmd == "/help":
        print("  /quit        — exit chat")
        print("  /reset       — clear history")
        print("  /lang <code> — switch language")
        print("  /langs       — list all languages")
        print("  /status      — show engine status")
        return True

    print(f"Unknown command: {cmd}. Type /help for available commands.")
    return True


def run_chat_cli(
    backend_name: str | None = None,
    profile_code: str | None = None,
    model: str | None = None,
) -> None:
    """Run the interactive chat REPL."""
    backend = _resolve_backend(backend_name)
    engine = ChatEngine(backend=backend, model=model)

    if profile_code:
        try:
            profile = load_profile(profile_code)
            if profile:
                engine.set_language(profile_code, profile["name"])
        except ValueError:
            print(f"Warning: Unknown profile '{profile_code}', using auto-detect.")

    _print_banner(engine)

    if not engine.backend.is_available():
        print("WARNING: The selected backend is not available.")
        print("For Ollama: install from https://ollama.com and run 'ollama serve'")
        print("For OpenAI: set OPENAI_API_KEY environment variable")
        print("For Anthropic: set ANTHROPIC_API_KEY environment variable")
        print("Falling back to echo mode for testing.\n")
        engine.backend = EchoBackend()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            if not _handle_command(engine, user_input):
                break
            continue

        try:
            response = engine.chat(user_input)
            print(f"\nPAT: {response}\n")
        except ConnectionError as exc:
            print(f"\nConnection error: {exc}")
            print("Make sure your LLM backend is running.\n")
        except Exception as exc:
            print(f"\nError: {exc}\n")
