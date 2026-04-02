"""PAT Chat Engine — manages conversation state, language detection, and LLM interaction."""
from __future__ import annotations

from dataclasses import dataclass, field

from pat_chat.backends import ChatBackend, ChatMessage, auto_select_backend
from pat_chat.detect import detect_language
from pat_chat.prompts import build_system_prompt
from pat_policy.policy import enforce_policy
from pat_validation.validator import validate_input


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

    def set_language(self, code: str, name: str) -> None:
        """Manually set the conversation language and disable auto-detect."""
        self.language_code = code
        self.language_name = name
        self.auto_detect = False

    def _detect_and_update(self, text: str) -> None:
        """Auto-detect language from user text and update if confident."""
        if not self.auto_detect:
            return
        result = detect_language(text)
        if result.confidence >= 0.6:
            self.language_code = result.code
            self.language_name = result.name

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
        Auto-detects language on each message, builds context-aware prompts,
        and maintains conversation history.

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

        return response

    def reset(self) -> None:
        """Clear conversation history and language state, re-enable auto-detect."""
        self.history.clear()
        self.language_code = None
        self.language_name = None
        self.auto_detect = True

    def status(self) -> dict:
        """Return current engine status."""
        return {
            "backend": self.backend.name(),
            "backend_available": self.backend.is_available(),
            "language_code": self.language_code,
            "language_name": self.language_name,
            "auto_detect": self.auto_detect,
            "history_length": len(self.history),
            "model": self.model,
        }
