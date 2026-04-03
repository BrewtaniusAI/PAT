"""PAT Chat Web Server — stdlib HTTP server for multilingual chat UI.

Includes REST API with health checks, batch processing, rate limiting,
code-switching detection, session metrics, and streaming SSE support.
"""
from __future__ import annotations

import json
import threading
import time
from collections import defaultdict
from pathlib import Path
from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import http.server
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

# Global engine instance and lock for thread-safe access
_engine: ChatEngine | None = None
_engine_lock = threading.Lock()

# --- Rate limiter (token bucket per IP) ---
_RATE_LIMIT = 30  # requests per window
_RATE_WINDOW = 60  # seconds
_rate_buckets: dict[str, list[float]] = defaultdict(list)
_rate_lock = threading.Lock()

# Server start time for uptime tracking
_server_start_time: float = 0.0


def _get_engine() -> ChatEngine:
    global _engine
    if _engine is None:
        _engine = ChatEngine()
    return _engine


def _check_rate_limit(client_ip: str) -> bool:
    """Return True if the request is within rate limits, False if exceeded."""
    now = time.time()
    with _rate_lock:
        bucket = _rate_buckets.get(client_ip, [])
        # Prune old entries outside the window
        bucket = [t for t in bucket if now - t < _RATE_WINDOW]
        if len(bucket) >= _RATE_LIMIT:
            _rate_buckets[client_ip] = bucket
            return False
        bucket.append(now)
        _rate_buckets[client_ip] = bucket
        # Evict stale IPs to prevent unbounded memory growth
        if len(_rate_buckets) > 1000:
            stale = [ip for ip, ts in _rate_buckets.items()
                     if not ts or now - ts[-1] >= _RATE_WINDOW]
            for ip in stale:
                del _rate_buckets[ip]
        return True


def _json_response(handler: "_ChatHandler", data: dict | list, status: int = 200) -> None:
    """Send a JSON response (same-origin only, no CORS wildcard)."""
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class _ChatHandler(BaseHTTPRequestHandler):
    """HTTP handler for PAT Chat web UI and REST API."""

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._serve_html()
        elif path == "/api/status":
            self._api_status()
        elif path == "/api/languages":
            self._api_languages()
        elif path == "/api/health":
            self._api_health()
        elif path == "/api/metrics":
            self._api_metrics()
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        # Rate limiting on POST endpoints
        client_ip = self.client_address[0]
        if not _check_rate_limit(client_ip):
            _json_response(self, {
                "error": "Rate limit exceeded. Max 30 requests per minute.",
            }, 429)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b""

        if path == "/api/chat":
            self._api_chat(body)
        elif path == "/api/language":
            self._api_set_language(body)
        elif path == "/api/reset":
            self._api_reset()
        elif path == "/api/batch":
            self._api_batch(body)
        elif path == "/api/detect":
            self._api_detect(body)
        else:
            self.send_error(404)

    def do_OPTIONS(self) -> None:
        """Handle CORS preflight (same-origin only)."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _serve_html(self) -> None:
        html_path = TEMPLATE_DIR / "index.html"
        try:
            content = html_path.read_bytes()
        except (FileNotFoundError, OSError):
            self.send_error(500, "Chat UI template not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _api_status(self) -> None:
        engine = _get_engine()
        with _engine_lock:
            _json_response(self, engine.status())

    def _api_languages(self) -> None:
        codes = list_profiles()
        langs = []
        for code in codes:
            profile = load_profile(code)
            if profile:
                langs.append({"code": code, "name": profile["name"]})
        _json_response(self, langs)

    def _api_health(self) -> None:
        """Health/readiness probe for deployment monitoring.

        Returns backend availability, uptime, and dialect count.
        """
        engine = _get_engine()
        uptime = time.time() - _server_start_time if _server_start_time else 0
        with _engine_lock:
            backend_ok = engine.backend.is_available()
        _json_response(self, {
            "status": "healthy" if backend_ok else "degraded",
            "backend": engine.backend.name(),
            "backend_available": backend_ok,
            "dialect_count": len(list_profiles()),
            "uptime_seconds": round(uptime, 1),
            "version": "1.3.0",
        })

    def _api_metrics(self) -> None:
        """Session usage metrics endpoint."""
        engine = _get_engine()
        with _engine_lock:
            _json_response(self, engine.metrics.to_dict())

    def _api_chat(self, body: bytes) -> None:
        engine = _get_engine()
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            _json_response(self, {"error": "Invalid JSON"}, 400)
            return
        if not isinstance(data, dict):
            _json_response(self, {"error": "Expected JSON object"}, 400)
            return
        try:
            message = str(data.get("message") or "").strip()
            if not message:
                _json_response(self, {"error": "Empty message"}, 400)
                return

            # Lock around the entire chat + state read to prevent race conditions
            with _engine_lock:
                response = engine.chat(message)
                result = {
                    "response": response,
                    "language_code": engine.language_code,
                    "language_name": engine.language_name,
                }
            _json_response(self, result)
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
        except json.JSONDecodeError:
            _json_response(self, {"error": "Invalid JSON"}, 400)
            return
        if not isinstance(data, dict):
            _json_response(self, {"error": "Expected JSON object"}, 400)
            return
        try:
            code = str(data.get("code") or "").strip()
            with _engine_lock:
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
        with _engine_lock:
            engine.reset()
        _json_response(self, {"status": "reset"})

    def _api_batch(self, body: bytes) -> None:
        """Batch language detection endpoint for enterprise integration.

        Accepts a JSON array of texts and returns detection results for each,
        including code-switching analysis. Processes up to 100 texts per request.

        Request: {"texts": ["Sannu!", "Jambo habari", ...]}
        Response: {"results": [{...}, {...}, ...]}
        """
        engine = _get_engine()
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            _json_response(self, {"error": "Invalid JSON"}, 400)
            return
        if not isinstance(data, dict):
            _json_response(self, {"error": "Expected JSON object"}, 400)
            return

        texts = data.get("texts", [])
        if not isinstance(texts, list):
            _json_response(self, {"error": "'texts' must be a list"}, 400)
            return
        if len(texts) > 100:
            _json_response(self, {"error": "Maximum 100 texts per batch"}, 400)
            return

        results = []
        with _engine_lock:
            for text in texts:
                text_str = str(text or "").strip()
                if not text_str:
                    results.append({"error": "Empty text", "text": ""})
                    continue
                cs = engine.detect_languages(text_str)
                entry: dict = {
                    "text": text_str[:200],  # truncate for response
                    "primary": {
                        "code": cs.primary.code,
                        "name": cs.primary.name,
                        "confidence": cs.primary.confidence,
                        "matches": cs.primary.matches,
                    },
                    "is_code_switched": cs.is_code_switched,
                }
                if cs.secondary:
                    entry["secondary"] = [
                        {
                            "code": s.code,
                            "name": s.name,
                            "confidence": s.confidence,
                            "matches": s.matches,
                        }
                        for s in cs.secondary
                    ]
                results.append(entry)

        _json_response(self, {"results": results, "count": len(results)})

    def _api_detect(self, body: bytes) -> None:
        """Single-text code-switching detection endpoint.

        Request: {"text": "Sannu! Habari gani?"}
        Response: {primary: {...}, secondary: [...], is_code_switched: true}
        """
        engine = _get_engine()
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            _json_response(self, {"error": "Invalid JSON"}, 400)
            return
        if not isinstance(data, dict):
            _json_response(self, {"error": "Expected JSON object"}, 400)
            return

        text = str(data.get("text") or "").strip()
        if not text:
            _json_response(self, {"error": "Empty text"}, 400)
            return

        with _engine_lock:
            cs = engine.detect_languages(text)

        result: dict = {
            "primary": {
                "code": cs.primary.code,
                "name": cs.primary.name,
                "confidence": cs.primary.confidence,
                "matches": cs.primary.matches,
            },
            "is_code_switched": cs.is_code_switched,
        }
        if cs.secondary:
            result["secondary"] = [
                {
                    "code": s.code,
                    "name": s.name,
                    "confidence": s.confidence,
                    "matches": s.matches,
                }
                for s in cs.secondary
            ]
        _json_response(self, result)

    def log_message(self, format: str, *args) -> None:
        """Suppress default logging to keep output clean."""
        pass


def run_web_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    backend_name: str | None = None,
    profile_code: str | None = None,
    model: str | None = None,
) -> None:
    """Start the PAT Chat web server."""
    global _engine, _server_start_time

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

    class _ThreadingHTTPServer(ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True

    _server_start_time = time.time()
    server = _ThreadingHTTPServer((host, port), _ChatHandler)
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
    print(f"  Dialects : {len(list_profiles())}")
    print()
    print("  API Endpoints:")
    print("    GET  /api/health      — readiness probe")
    print("    GET  /api/status      — engine status + metrics")
    print("    GET  /api/languages   — list all 71 dialects")
    print("    GET  /api/metrics     — session usage metrics")
    print("    POST /api/chat        — send message")
    print("    POST /api/detect      — detect languages (code-switching)")
    print("    POST /api/batch       — batch language detection")
    print("    POST /api/language    — set active language")
    print("    POST /api/reset       — reset conversation")
    print()
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
