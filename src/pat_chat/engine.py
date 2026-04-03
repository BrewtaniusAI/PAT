"""PAT Chat Engine — manages conversation state, language detection, and LLM interaction.

Supports code-switching detection (multiple languages in a single text) and
tracks usage metrics per session for telemetry.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from pat_chat.backends import ChatBackend, ChatMessage, auto_select_backend
from pat_chat.detect import CodeSwitchResult, detect_code_switching
from pat_chat.prompts import build_system_prompt
from pat_policy.policy import enforce_policy
from pat_validation.validator import validate_input


@dataclass
class SessionMetrics:
    """Lightweight usage metrics for a single chat session."""

    total_messages: int = 0
    total_input_chars: int = 0
    total_output_chars: int = 0
    languages_seen: set[str] = field(default_factory=set)
    code_switches_detected: int = 0
    started_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        elapsed = time.time() - self.started_at
        return {
            "total_messages": self.total_messages,
            "total_input_chars": self.total_input_chars,
            "total_output_chars": self.total_output_chars,
            "languages_seen": sorted(self.languages_seen),
            "code_switches_detected": self.code_switches_detected,
            "session_duration_seconds": round(elapsed, 1),
        }


@dataclass
class ChatEngine:
    """Stateful chat engine with auto language detection and pluggable backends."""

    backend: ChatBackend = field(default_factory=auto_select_backend)
    language_code: str | None = None
    language_name: str | None = None
    auto_detect: bool = True
    history: list[ChatMessage] = field(default_factory=list)
    model: str | None = None
    max_history: int = 50
    metrics: SessionMetrics = field(default_factory=SessionMetrics)

    def set_language(self, code: str, name: str) -> None:
        """Manually set the conversation language and disable auto-detect."""
        self.language_code = code
        self.language_name = name
        self.auto_detect = False

    def _detect_and_update(self, text: str) -> CodeSwitchResult | None:
        """Auto-detect language from user text and update if confident.

        Returns code-switching result if detection ran, None if skipped.
        """
        if not self.auto_detect:
            return None
        cs_result = detect_code_switching(text)

        if cs_result.primary.confidence >= 0.6:
            self.language_code = cs_result.primary.code
            self.language_name = cs_result.primary.name

        # Track all detected languages and code-switching events
        if cs_result.primary.code != "unknown":
            self.metrics.languages_seen.add(cs_result.primary.code)
        for sec in cs_result.secondary:
            self.metrics.languages_seen.add(sec.code)
        if cs_result.is_code_switched:
            self.metrics.code_switches_detected += 1

        return cs_result

    def _build_messages(self, user_text: str) -> list[ChatMessage]:
        """Build the full message list including system prompt and recent history."""
        system_prompt = build_system_prompt(self.language_code, self.language_name)
        messages = [ChatMessage(role="system", content=system_prompt)]
        # Sliding window: keep only the most recent messages
        recent = self.history[-self.max_history:] if len(self.history) > self.max_history else self.history
        messages.extend(recent)
        messages.append(ChatMessage(role="user", content=user_text))
        return messages

    def chat(self, user_text: str) -> str:
        """Send a message and get a response.

        Enforces input validation and policy checks before processing.
        Auto-detects language on each message (including code-switching),
        builds context-aware prompts, and maintains conversation history.

        Raises:
            ValueError: If input fails validation (empty, too long).
            PermissionError: If input violates policy (forbidden patterns).
        """
        validate_input(user_text)
        enforce_policy(user_text)

        self._detect_and_update(user_text)
        messages = self._build_messages(user_text)
        response = self.backend.generate(messages, model=self.model)

        # Update history and trim to max_history to prevent unbounded growth
        self.history.append(ChatMessage(role="user", content=user_text))
        self.history.append(ChatMessage(role="assistant", content=response))
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        # Update metrics
        self.metrics.total_messages += 1
        self.metrics.total_input_chars += len(user_text)
        self.metrics.total_output_chars += len(response)

        return response

    def detect_languages(self, text: str) -> CodeSwitchResult:
        """Public API: detect all languages in text (code-switching aware).

        Does NOT modify engine state — purely diagnostic.
        """
        return detect_code_switching(text)

    def reset(self) -> None:
        """Clear conversation history and language state, re-enable auto-detect."""
        self.history.clear()
        self.language_code = None
        self.language_name = None
        self.auto_detect = True
        self.metrics = SessionMetrics()

    def status(self) -> dict:
        """Return current engine status including session metrics."""
        return {
            "backend": self.backend.name(),
            "backend_available": self.backend.is_available(),
            "language_code": self.language_code,
            "language_name": self.language_name,
            "auto_detect": self.auto_detect,
            "history_length": len(self.history),
            "model": self.model,
            "metrics": self.metrics.to_dict(),
        }
