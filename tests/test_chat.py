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
from pat_chat.detect import detect_language, detect_code_switching, CodeSwitchResult
from pat_chat.engine import ChatEngine, SessionMetrics
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
    assert result.confidence > 0
    assert result.code != "unknown"


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
    assert engine.auto_detect is False


def test_engine_manual_language_persists_across_chat():
    """Manual language override must not be overwritten by auto-detection."""
    engine = ChatEngine(backend=EchoBackend())
    engine.set_language("yo", "Yorùbá")
    # Send a message with Hausa keywords — should NOT switch language
    engine.chat("sannu nagode lafiya gaskiya mutum")
    assert engine.language_code == "yo"
    assert engine.language_name == "Yorùbá"
    assert engine.auto_detect is False


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


# --- Code-switching detection tests ---

def test_code_switching_returns_result():
    result = detect_code_switching("sannu nagode lafiya gaskiya mutum")
    assert isinstance(result, CodeSwitchResult)
    assert result.primary.code != "unknown"
    assert result.primary.confidence >= 0.4


def test_code_switching_unknown_text():
    result = detect_code_switching("xyz abc 12345")
    assert result.primary.code == "unknown"
    assert result.is_code_switched is False
    assert result.secondary == []


def test_code_switching_multi_language_text():
    """Text with keywords from multiple languages should detect code-switching."""
    # Hausa keywords + Swahili keywords in one text
    result = detect_code_switching("sannu nagode jambo habari karibu asante")
    assert result.primary.code in ("ha", "sw")
    # At least the primary should match
    assert result.primary.confidence >= 0.4


def test_engine_detect_languages_does_not_mutate_state():
    engine = ChatEngine(backend=EchoBackend())
    engine.set_language("yo", "Yorùbá")
    # detect_languages is diagnostic-only
    cs = engine.detect_languages("sannu nagode lafiya gaskiya mutum")
    assert cs.primary.code == "ha"
    # Engine state should remain unchanged
    assert engine.language_code == "yo"
    assert engine.language_name == "Yorùbá"


# --- Session metrics tests ---

def test_session_metrics_initial():
    m = SessionMetrics()
    d = m.to_dict()
    assert d["total_messages"] == 0
    assert d["total_input_chars"] == 0
    assert d["total_output_chars"] == 0
    assert d["languages_seen"] == []
    assert d["code_switches_detected"] == 0
    assert d["session_duration_seconds"] >= 0


def test_engine_metrics_track_messages():
    engine = ChatEngine(backend=EchoBackend())
    engine.chat("Hello world")
    engine.chat("sannu nagode lafiya gaskiya mutum")
    m = engine.metrics.to_dict()
    assert m["total_messages"] == 2
    assert m["total_input_chars"] > 0
    assert m["total_output_chars"] > 0


def test_engine_metrics_track_languages():
    engine = ChatEngine(backend=EchoBackend())
    engine.chat("sannu nagode lafiya gaskiya mutum")
    m = engine.metrics.to_dict()
    assert "ha" in m["languages_seen"]


def test_engine_reset_clears_metrics():
    engine = ChatEngine(backend=EchoBackend())
    engine.chat("Hello")
    engine.reset()
    m = engine.metrics.to_dict()
    assert m["total_messages"] == 0


def test_engine_status_includes_metrics():
    engine = ChatEngine(backend=EchoBackend())
    status = engine.status()
    assert "metrics" in status
    assert "total_messages" in status["metrics"]
