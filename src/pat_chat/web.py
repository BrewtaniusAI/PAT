"""PAT Chat Web Server — stdlib HTTP server for multilingual chat UI."""
from __future__ import annotations

import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

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

TEMPLATE_DIR = Path(__file__).parent / "templates"

# Global engine instance for the web server
_engine: ChatEngine | None = None


def _get_engine() -> ChatEngine:
    global _engine
    if _engine is None:
        _engine = ChatEngine()
    return _engine


def _json_response(handler: "_ChatHandler", data: dict | list, status: int = 200) -> None:
    """Send a JSON response."""
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


class _ChatHandler(SimpleHTTPRequestHandler):
    """HTTP handler for PAT Chat web UI."""

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._serve_html()
        elif path == "/api/status":
            self._api_status()
        elif path == "/api/languages":
            self._api_languages()
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b""

        if path == "/api/chat":
            self._api_chat(body)
        elif path == "/api/language":
            self._api_set_language(body)
        elif path == "/api/reset":
            self._api_reset()
        else:
            self.send_error(404)

    def do_OPTIONS(self) -> None:
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _serve_html(self) -> None:
        html_path = TEMPLATE_DIR / "index.html"
        content = html_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _api_status(self) -> None:
        engine = _get_engine()
        _json_response(self, engine.status())

    def _api_languages(self) -> None:
        codes = list_profiles()
        langs = []
        for code in codes:
            profile = load_profile(code)
            if profile:
                langs.append({"code": code, "name": profile["name"]})
        _json_response(self, langs)

    def _api_chat(self, body: bytes) -> None:
        engine = _get_engine()
        try:
            data = json.loads(body) if body else {}
            message = data.get("message", "").strip()
            if not message:
                _json_response(self, {"error": "Empty message"}, 400)
                return

            response = engine.chat(message)
            _json_response(self, {
                "response": response,
                "language_code": engine.language_code,
                "language_name": engine.language_name,
            })
        except PermissionError as exc:
            _json_response(self, {"error": str(exc)}, 403)
        except ValueError as exc:
            _json_response(self, {"error": str(exc)}, 400)
        except ConnectionError as exc:
            _json_response(self, {"error": str(exc)}, 503)
        except Exception as exc:
            _json_response(self, {"error": str(exc)}, 500)

    def _api_set_language(self, body: bytes) -> None:
        engine = _get_engine()
        try:
            data = json.loads(body) if body else {}
            code = data.get("code", "").strip()
            if not code:
                engine.language_code = None
                engine.language_name = None
                engine.auto_detect = True
                _json_response(self, {"status": "auto-detect"})
                return

            profile = load_profile(code)
            if profile:
                engine.set_language(code, profile["name"])
                _json_response(self, {
                    "status": "ok",
                    "code": code,
                    "name": profile["name"],
                })
            else:
                _json_response(self, {"error": f"Unknown language: {code}"}, 400)
        except (ValueError, KeyError) as exc:
            _json_response(self, {"error": str(exc)}, 400)

    def _api_reset(self) -> None:
        engine = _get_engine()
        engine.reset()
        _json_response(self, {"status": "reset"})

    def log_message(self, format: str, *args) -> None:
        """Suppress default logging to keep output clean."""
        pass


def run_web_server(
    host: str = "0.0.0.0",
    port: int = 8080,
    backend_name: str | None = None,
    profile_code: str | None = None,
    model: str | None = None,
) -> None:
    """Start the PAT Chat web server."""
    global _engine

    # Resolve backend
    if backend_name:
        name = backend_name.lower()
        if name == "ollama":
            backend: ChatBackend = OllamaBackend()
        elif name == "openai":
            backend = OpenAIBackend()
        elif name == "anthropic":
            backend = AnthropicBackend()
        elif name == "echo":
            backend = EchoBackend()
        else:
            backend = auto_select_backend()
    else:
        backend = auto_select_backend()

    _engine = ChatEngine(backend=backend, model=model)

    if profile_code:
        try:
            profile = load_profile(profile_code)
            if profile:
                _engine.set_language(profile_code, profile["name"])
        except ValueError:
            pass

    server = HTTPServer((host, port), _ChatHandler)
    status = _engine.status()

    print()
    print("=" * 60)
    print("  PAT Chat Web Server")
    print("=" * 60)
    print(f"  URL     : http://{host}:{port}")
    print(f"  Backend : {status['backend']}")
    print(f"  Available: {status['backend_available']}")
    if _engine.language_code:
        print(f"  Language : {_engine.language_name} ({_engine.language_code})")
    print()
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
