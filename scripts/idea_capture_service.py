#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from rag_lib import generate_text


def capture_model() -> str:
    return os.environ.get("IDEA_CAPTURE_MODEL", "llama3.1:8b")


def capture_notes_dir() -> Path:
    return Path(os.environ.get("IDEA_CAPTURE_NOTES_DIR", "notes/idea-inbox")).expanduser().resolve()


def capture_token() -> str:
    return os.environ.get("IDEA_CAPTURE_API_TOKEN", "").strip()


def brainstorm_prompt(idea: str) -> str:
    return (
        "You turn rough personal idea captures into compact, useful brainstorm notes.\n"
        "Keep the output grounded in the user's wording. Do not invent a full product spec.\n"
        "Use this exact markdown section format:\n"
        "## Clean Summary\n"
        "- 2 to 4 bullets\n"
        "## Possible Directions\n"
        "- 2 to 5 bullets\n"
        "## Next Steps\n"
        "- 1 to 3 bullets\n\n"
        f"Raw idea:\n{idea}\n\n"
        "Structured note:"
    )


def normalize_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


class IdeaCaptureHandler(BaseHTTPRequestHandler):
    server: "IdeaCaptureServer"

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json(
                {
                    "ok": True,
                    "notes_dir": str(self.server.notes_dir),
                    "model": self.server.model,
                    "token_required": bool(self.server.api_token),
                }
            )
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        if self.path != "/capture":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        if not self.server.is_authorized(self.headers.get("Authorization", ""), self.headers.get("X-API-Key", "")):
            self.send_error(HTTPStatus.UNAUTHORIZED, "Unauthorized")
            return

        try:
            body = self.read_json()
        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON body")
            return

        idea = normalize_text(body.get("idea"))
        if not idea:
            self.send_error(HTTPStatus.BAD_REQUEST, "idea is required")
            return

        source = normalize_text(body.get("source")) or "manual"
        title = normalize_text(body.get("title"))

        try:
            structured = generate_text(brainstorm_prompt(idea), self.server.model)
            result = self.server.append_entry(idea=idea, structured=structured, source=source, title=title)
        except Exception as exc:  # pragma: no cover - defensive service boundary
            self.send_error(HTTPStatus.BAD_GATEWAY, f"Capture failed: {exc}")
            return

        self.send_json(
            {
                "ok": True,
                "file": str(result["file"]),
                "timestamp": result["timestamp"],
                "title": result["title"],
                "entry": result["entry"],
            },
            status=HTTPStatus.CREATED,
        )

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


class IdeaCaptureServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], handler: type[IdeaCaptureHandler], notes_dir: Path, model: str, api_token: str) -> None:
        super().__init__(server_address, handler)
        self.notes_dir = notes_dir
        self.model = model
        self.api_token = api_token
        self.write_lock = threading.Lock()

    def is_authorized(self, authorization_header: str, api_key_header: str) -> bool:
        if not self.api_token:
            return True

        bearer = authorization_header.strip()
        if bearer.startswith("Bearer ") and bearer[7:].strip() == self.api_token:
            return True
        if api_key_header.strip() == self.api_token:
            return True
        return False

    def append_entry(self, idea: str, structured: str, source: str, title: str) -> dict:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S %Z")
        day = time.strftime("%Y-%m-%d")
        file_path = self.notes_dir / f"{day}.md"
        safe_title = title or first_line(idea)
        entry = (
            f"## {safe_title}\n"
            f"- Captured: {timestamp}\n"
            f"- Source: {source}\n\n"
            f"### Raw Idea\n{idea}\n\n"
            f"{structured.strip()}\n\n"
        )

        with self.write_lock:
            self.notes_dir.mkdir(parents=True, exist_ok=True)
            with file_path.open("a", encoding="utf-8") as handle:
                handle.write(entry)

        return {"file": file_path, "timestamp": timestamp, "title": safe_title, "entry": entry}


def first_line(text: str) -> str:
    line = text.splitlines()[0].strip()
    if len(line) <= 72:
        return line
    return f"{line[:69].rstrip()}..."


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the idea capture service.")
    parser.add_argument("--host", default=os.environ.get("IDEA_CAPTURE_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("IDEA_CAPTURE_PORT", "8790")))
    parser.add_argument("--notes-dir", default=str(capture_notes_dir()))
    parser.add_argument("--model", default=capture_model())
    args = parser.parse_args()

    notes_dir = Path(args.notes_dir).expanduser().resolve()
    server = IdeaCaptureServer((args.host, args.port), IdeaCaptureHandler, notes_dir, args.model, capture_token())
    print(f"Idea capture service listening on http://{args.host}:{args.port}")
    print(f"Notes directory: {notes_dir}")
    print(f"Model: {args.model}")
    print(f"Token required: {'yes' if server.api_token else 'no'}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
