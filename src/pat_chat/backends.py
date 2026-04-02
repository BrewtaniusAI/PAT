"""Pluggable LLM backends for PAT chat.

All backends use only stdlib (urllib) — zero external dependencies.
OpenAI and Anthropic backends require API keys but no third-party libraries.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    role: str  # "system" | "user" | "assistant"
    content: str


class ChatBackend(ABC):
    """Base class for all LLM backends."""

    @abstractmethod
    def generate(self, messages: list[ChatMessage], model: str | None = None) -> str:
        """Send messages and return the assistant's reply text."""

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if this backend is ready to use."""

    @abstractmethod
    def name(self) -> str:
        """Human-readable backend name."""


class OllamaBackend(ChatBackend):
    """Local Ollama backend — no API key required.

    Communicates via HTTP to a locally running Ollama server.
    Default model: llama3.2 (small, runs on most hardware).
    """

    DEFAULT_MODEL = "llama3.2"

    def __init__(
        self,
        base_url: str | None = None,
        default_model: str | None = None,
    ) -> None:
        self.base_url = (
            base_url
            or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        )
        self.default_model = default_model or self.DEFAULT_MODEL

    def name(self) -> str:
        return f"Ollama ({self.default_model})"

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(
                f"{self.base_url}/api/tags",
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except (urllib.error.URLError, OSError):
            return False

    def generate(self, messages: list[ChatMessage], model: str | None = None) -> str:
        model = model or self.default_model
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return body.get("message", {}).get("content", "")
        except urllib.error.URLError as exc:
            raise ConnectionError(
                f"Ollama not reachable at {self.base_url}. "
                "Install from https://ollama.com and run: ollama serve"
            ) from exc


class OpenAIBackend(ChatBackend):
    """OpenAI-compatible backend (works with OpenAI, Azure, or any compatible API)."""

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        default_model: str | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = (
            base_url
            or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
        self.default_model = default_model or self.DEFAULT_MODEL

    def name(self) -> str:
        return f"OpenAI ({self.default_model})"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, messages: list[ChatMessage], model: str | None = None) -> str:
        model = model or self.default_model
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]


class AnthropicBackend(ChatBackend):
    """Anthropic Claude backend."""

    DEFAULT_MODEL = "claude-sonnet-4-20250514"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.default_model = default_model or self.DEFAULT_MODEL

    def name(self) -> str:
        return f"Anthropic ({self.default_model})"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, messages: list[ChatMessage], model: str | None = None) -> str:
        model = model or self.default_model
        system_text = ""
        api_messages = []
        for m in messages:
            if m.role == "system":
                system_text += m.content + "\n"
            else:
                api_messages.append({"role": m.role, "content": m.content})
        payload: dict = {
            "model": model,
            "max_tokens": 4096,
            "messages": api_messages,
        }
        if system_text.strip():
            payload["system"] = system_text.strip()
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["content"][0]["text"]


class EchoBackend(ChatBackend):
    """Testing backend that echoes input with language metadata. No LLM needed."""

    def name(self) -> str:
        return "Echo (testing)"

    def is_available(self) -> bool:
        return True

    def generate(self, messages: list[ChatMessage], model: str | None = None) -> str:
        user_msgs = [m for m in messages if m.role == "user"]
        last = user_msgs[-1].content if user_msgs else ""
        system_msgs = [m for m in messages if m.role == "system"]
        lang_hint = ""
        if system_msgs:
            first_line = system_msgs[0].content.split("\n")[0]
            lang_hint = f" [{first_line}]"
        return f"[echo]{lang_hint} {last}"


def auto_select_backend() -> ChatBackend:
    """Pick the best available backend automatically.

    Priority: OpenAI (if key set) > Anthropic (if key set) > Ollama (local) > Echo (fallback).
    """
    openai = OpenAIBackend()
    if openai.is_available():
        return openai

    anthropic = AnthropicBackend()
    if anthropic.is_available():
        return anthropic

    ollama = OllamaBackend()
    if ollama.is_available():
        return ollama

    return EchoBackend()
