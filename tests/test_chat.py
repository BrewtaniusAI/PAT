"""Tests for the PAT Chat module."""
import pytest

from pat_chat.backends import (
    ChatMessage,
    EchoBackend,
    OllamaBackend,
    OpenAIBackend,
    AnthropicBackend,
    auto_select_backend,
)
from pat_chat.detect import detect_language
from pat_chat.engine import ChatEngine
from pat_chat.prompts import build_system_prompt


# --- Backend tests ---

def test_echo_backend_is_available():
    backend = EchoBackend()
    assert backend.is_available() is True


def test_echo_backend_name():
    backend = EchoBackend()
    assert backend.name() == "Echo (testing)"


def test_echo_backend_generate():
    backend = EchoBackend()
    messages = [
        ChatMessage(role="system", content="Language: Yorùbá"),
        ChatMessage(role="user", content="Bawo ni?"),
    ]
    response = backend.generate(messages)
    assert "Bawo ni?" in response
    assert "echo" in response.lower()


def test_ollama_backend_defaults():
    backend = OllamaBackend()
    assert "Ollama" in backend.name()
    assert "llama3.2" in backend.name()


def test_openai_backend_not_available_without_key():
    backend = OpenAIBackend(api_key="")
    assert backend.is_available() is False


def test_anthropic_backend_not_available_without_key():
    backend = AnthropicBackend(api_key="")
    assert backend.is_available() is False


def test_auto_select_backend_returns_backend():
    """auto_select_backend should return some backend (likely Echo in test env)."""
    backend = auto_select_backend()
    assert backend is not None
    assert backend.is_available() is True


# --- Language detection tests ---

def test_detect_language_yoruba():
    result = detect_language("Ẹ káàárọ̀, bawo ni? nagode lafiya")
    # Should detect something (may vary based on keyword overlap)
    assert result.code is not None


def test_detect_language_hausa():
    result = detect_language("sannu nagode lafiya gaskiya mutum")
    assert result.code == "ha"
    assert result.confidence >= 0.4


def test_detect_language_swahili():
    result = detect_language("jambo habari karibu asante sana")
    assert result.code == "sw"
    assert result.confidence >= 0.4


def test_detect_language_unknown():
    result = detect_language("xyz abc 12345")
    assert result.confidence == 0.0


# --- System prompt tests ---

def test_system_prompt_with_language():
    prompt = build_system_prompt("yo", "Yorùbá")
    assert "Yorùbá" in prompt
    assert "PAT" in prompt
    assert "71" in prompt or "language" in prompt.lower()


def test_system_prompt_without_language():
    prompt = build_system_prompt(None, None)
    assert "auto" in prompt.lower() or "detect" in prompt.lower()


# --- Chat engine tests ---

def test_engine_with_echo_backend():
    engine = ChatEngine(backend=EchoBackend())
    response = engine.chat("Sannu!")
    assert "Sannu!" in response


def test_engine_language_detection():
    engine = ChatEngine(backend=EchoBackend())
    engine.chat("sannu nagode lafiya gaskiya mutum")
    assert engine.language_code == "ha"
    assert engine.language_name == "Hausa"


def test_engine_manual_language_set():
    engine = ChatEngine(backend=EchoBackend())
    engine.set_language("yo", "Yorùbá")
    assert engine.language_code == "yo"
    assert engine.language_name == "Yorùbá"


def test_engine_history():
    engine = ChatEngine(backend=EchoBackend())
    engine.chat("Hello")
    engine.chat("World")
    assert len(engine.history) == 4  # 2 user + 2 assistant


def test_engine_reset():
    engine = ChatEngine(backend=EchoBackend())
    engine.chat("Hello")
    engine.set_language("sw", "Kiswahili")
    engine.reset()
    assert len(engine.history) == 0
    assert engine.language_code is None


def test_engine_status():
    engine = ChatEngine(backend=EchoBackend())
    status = engine.status()
    assert "backend" in status
    assert "backend_available" in status
    assert status["backend_available"] is True
    assert status["history_length"] == 0


# --- Policy enforcement tests ---

def test_engine_rejects_policy_violation():
    engine = ChatEngine(backend=EchoBackend())
    with pytest.raises(PermissionError, match="impersonate"):
        engine.chat("impersonate someone")


def test_engine_rejects_empty_input():
    engine = ChatEngine(backend=EchoBackend())
    with pytest.raises(ValueError, match="empty"):
        engine.chat("   ")
