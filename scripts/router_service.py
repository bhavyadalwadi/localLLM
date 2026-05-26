#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from rag_lib import (
    RagRuntime,
    build_answer_prompt,
    chat_model,
    generate_text,
    generate_text_with_images,
    index_path,
    load_json,
    rank_items,
    top_k,
)


AUTO_MODEL_NAME = "local-ai-node-auto"


def code_model() -> str:
    import os

    return os.environ.get("ROUTER_CODE_MODEL", "deepseek-coder:6.7b")


def light_model() -> str:
    import os

    return os.environ.get("ROUTER_LIGHT_MODEL", "phi3")


def rag_model() -> str:
    import os

    return os.environ.get("ROUTER_RAG_MODEL", "gemma4:31b")


def default_model() -> str:
    import os

    return os.environ.get("ROUTER_DEFAULT_MODEL", chat_model())


def vision_model() -> str:
    import os

    return os.environ.get("ROUTER_VISION_MODEL", "llava:13b")


def message_to_text(message: dict) -> str:
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "\n".join(part for part in parts if part).strip()
    return ""


def message_image_refs(message: dict) -> list[str]:
    content = message.get("content", "")
    if not isinstance(content, list):
        return []

    images = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") not in {"image_url", "input_image"}:
            continue

        image_url = item.get("image_url")
        if isinstance(image_url, dict):
            url = str(image_url.get("url", "")).strip()
        else:
            url = str(image_url or item.get("image") or "").strip()
        if url:
            images.append(url)
    return images


def extract_last_user_text(messages: list[dict]) -> str:
    for message in reversed(messages):
        if message.get("role") == "user":
            return message_to_text(message).strip()
    return ""


def extract_last_user_images(messages: list[dict]) -> list[str]:
    for message in reversed(messages):
        if message.get("role") == "user":
            images = message_image_refs(message)
            if images:
                return images
    return []


def extract_recent_conversation_text(messages: list[dict], limit: int = 6) -> str:
    recent = messages[-limit:]
    parts = []
    for message in recent:
        text = message_to_text(message).strip()
        if not text:
            continue
        parts.append(text)
    return "\n".join(parts).strip()


def extract_recent_history(messages: list[dict], limit: int = 6) -> list[tuple[str, str]]:
    recent = messages[-limit:]
    if recent and recent[-1].get("role") == "user":
        recent = recent[:-1]

    history: list[tuple[str, str]] = []
    for message in recent:
        text = message_to_text(message).strip()
        if text:
            history.append((str(message.get("role", "user")), text))
    return history


def render_messages_as_prompt(messages: list[dict]) -> str:
    sections = []
    for message in messages:
        text = message_to_text(message).strip()
        if not text:
            continue
        role = message.get("role", "user").upper()
        sections.append(f"{role}:\n{text}")
    return "\n\n".join(sections).strip()


def count_keyword_hits(text: str, keywords: set[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def weighted_history_score(history: list[tuple[str, str]], keywords: set[str]) -> float:
    total = 0.0
    for index, (role, text) in enumerate(reversed(history)):
        weight = max(0.4, 1.5 - (index * 0.25))
        if role == "assistant":
            weight *= 0.8
        total += count_keyword_hits(text.lower(), keywords) * weight
    return total


def is_follow_up_query(query: str) -> bool:
    lowered = query.lower()
    if not lowered:
        return False

    follow_up_phrases = {
        "what about",
        "how about",
        "keep going",
        "go on",
        "continue",
        "same thing",
        "same for",
        "that one",
        "this one",
    }
    if any(phrase in lowered for phrase in follow_up_phrases):
        return True

    tokens = re.findall(r"[a-z0-9']+", lowered)
    if not tokens:
        return False
    referential_tokens = {
        "that",
        "this",
        "it",
        "those",
        "these",
        "they",
        "them",
        "same",
        "also",
        "instead",
        "again",
    }
    return len(tokens) <= 10 and any(token in referential_tokens for token in tokens)


def classify_route(query: str, messages: list[dict]) -> tuple[str, str, str]:
    lowered = query.lower()
    code_keywords = {
        "code",
        "python",
        "javascript",
        "typescript",
        "bug",
        "stack trace",
        "function",
        "class",
        "refactor",
        "implement",
        "sql",
        "bash",
        "shell",
        "api",
        "test",
    }
    rag_keywords = {
        "our",
        "this repo",
        "this node",
        "architecture",
        "deployment",
        "target host",
        "migration",
        "security",
        "performance",
        "open webui",
        "ollama",
        "readme",
        "docs",
        "rag",
        "backup",
        "restore",
        "model roles",
    }
    light_keywords = {"quick", "brief", "one line", "short answer"}

    history = extract_recent_history(messages)
    follow_up = is_follow_up_query(query)

    code_query_score = count_keyword_hits(lowered, code_keywords) * 3
    rag_query_score = count_keyword_hits(lowered, rag_keywords) * 3
    code_score = code_query_score + weighted_history_score(history, code_keywords)
    rag_score = rag_query_score + weighted_history_score(history, rag_keywords)

    if code_query_score >= 3 and code_score > rag_score + 1:
        return ("code", code_model(), f"coding score {code_score:.1f}")
    if rag_query_score >= 3 and rag_score > code_score + 1:
        return ("rag", rag_model(), f"local-knowledge score {rag_score:.1f}")

    if follow_up:
        if code_score >= 2.5 and code_score > rag_score + 0.5:
            return ("code", code_model(), f"follow-up coding score {code_score:.1f}")
        if rag_score >= 2.5 and rag_score > code_score + 0.5:
            return ("rag", rag_model(), f"follow-up local-knowledge score {rag_score:.1f}")

    if code_query_score > 0 and code_score >= 3 and code_score > rag_score + 0.5:
        return ("code", code_model(), f"coding score {code_score:.1f}")
    if rag_query_score > 0 and rag_score >= 3 and rag_score > code_score + 0.5:
        return ("rag", rag_model(), f"local-knowledge score {rag_score:.1f}")

    if len(lowered.split()) <= 8 or any(keyword in lowered for keyword in light_keywords):
        return ("light", light_model(), "short utility prompt")
    return ("chat", default_model(), "default chat fallback")


def classify_route_with_images(query: str, messages: list[dict], image_refs: list[str]) -> tuple[str, str, str]:
    if image_refs:
        return ("vision", vision_model(), f"image input detected ({len(image_refs)} image(s))")
    return classify_route(query, messages)


def build_rag_response(server: "RouterServer", query: str, model: str, limit: int) -> tuple[str, list[dict]]:
    if server.rag_runtime is not None:
        return server.rag_runtime.answer(query, model=model, limit=limit)

    payload = load_json(server.index_file)
    items = payload.get("items", [])
    if not items:
        raise RuntimeError("RAG index is empty. Build it first.")
    chunks = rank_items(query, items, limit, payload.get("embedding_model"))
    prompt = build_answer_prompt(query, chunks)
    answer = generate_text(prompt, model)
    return answer, chunks


def build_direct_response(messages: list[dict], model: str, image_refs: list[str] | None = None) -> str:
    prompt = (
        "Respond directly to the conversation below. "
        "Be concise but useful. If the user is asking about the local node or repo, "
        "do not invent facts that are not present in the conversation.\n\n"
        f"{render_messages_as_prompt(messages)}\n\nASSISTANT:"
    )
    if image_refs:
        prompt = (
            "The conversation includes image input. Use the images together with the text. "
            "If the user asks what is in the image, answer from the image rather than guessing.\n\n"
            f"{prompt}"
        )
        return generate_text_with_images(prompt, image_refs, model)
    return generate_text(prompt, model)


def build_chat_result(server: "RouterServer", messages: list[dict], preferred_model: str | None = None, limit: int | None = None) -> dict:
    query = extract_last_user_text(messages)
    image_refs = extract_last_user_images(messages)
    if not query and not image_refs:
        raise ValueError("No user message found.")
    if not query and image_refs:
        query = "Describe the provided image."

    route, selected_model, reason = classify_route_with_images(query, messages, image_refs)
    if preferred_model and preferred_model not in {AUTO_MODEL_NAME, ""}:
        selected_model = preferred_model
        route = "manual"
        reason = "explicit model override"

    if route == "rag" and server.index_exists():
        answer, chunks = build_rag_response(server, query, selected_model, limit or top_k())
        sources = [
            {
                "path": item["path"],
                "chunk_index": item["chunk_index"],
                "score": item["score"],
                "semantic_score": item["semantic_score"],
                "lexical_score": item["lexical_score"],
            }
            for item in chunks
        ]
    else:
        if route == "rag" and not server.index_exists():
            route = "chat"
            selected_model = default_model()
            reason = "RAG requested but index missing; fell back to default chat"
        answer = build_direct_response(messages, selected_model, image_refs=image_refs)
        sources = []

    return {
        "route": route,
        "reason": reason,
        "model": selected_model,
        "answer": answer,
        "sources": sources,
    }


def openai_chat_response(result: dict, requested_model: str) -> dict:
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": requested_model or AUTO_MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": result["answer"]},
                "finish_reason": "stop",
            }
        ],
        "router": {
            "route": result["route"],
            "selected_model": result["model"],
            "reason": result["reason"],
            "sources": result["sources"],
        },
    }


class RouterHandler(BaseHTTPRequestHandler):
    server: "RouterServer"

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json(
                {
                    "ok": True,
                    "index_path": str(self.server.index_file),
                    "default_model": default_model(),
                    "code_model": code_model(),
                    "light_model": light_model(),
                    "rag_model": rag_model(),
                }
            )
            return

        if self.path == "/v1/models":
            self.send_json(
                {
                    "object": "list",
                    "data": [
                        {"id": AUTO_MODEL_NAME, "object": "model", "owned_by": "local"},
                        {"id": default_model(), "object": "model", "owned_by": "local"},
                        {"id": code_model(), "object": "model", "owned_by": "local"},
                        {"id": light_model(), "object": "model", "owned_by": "local"},
                        {"id": rag_model(), "object": "model", "owned_by": "local"},
                        {"id": vision_model(), "object": "model", "owned_by": "local"},
                    ],
                }
            )
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        body = self.read_json()

        if self.path == "/chat":
            question = str(body.get("question", "")).strip()
            if not question:
                self.send_error(HTTPStatus.BAD_REQUEST, "question is required")
                return
            messages = [{"role": "user", "content": question}]
            result = build_chat_result(
                self.server,
                messages,
                preferred_model=body.get("model"),
                limit=int(body.get("top_k", top_k())),
            )
            self.send_json(result)
            return

        if self.path == "/v1/chat/completions":
            messages = body.get("messages", [])
            if not isinstance(messages, list) or not messages:
                self.send_error(HTTPStatus.BAD_REQUEST, "messages are required")
                return
            requested_model = body.get("model", AUTO_MODEL_NAME)
            result = build_chat_result(
                self.server,
                messages,
                preferred_model=requested_model,
                limit=int(body.get("top_k", top_k())),
            )
            if body.get("stream") is True:
                self.send_openai_stream(result, requested_model)
            else:
                self.send_json(openai_chat_response(result, requested_model))
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

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

    def send_openai_stream(self, result: dict, requested_model: str) -> None:
        completion_id = f"chatcmpl-{uuid.uuid4().hex}"
        created = int(time.time())
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        content = result["answer"]
        for chunk in content.split():
            payload = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": requested_model or AUTO_MODEL_NAME,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": f"{chunk} "},
                        "finish_reason": None,
                    }
                ],
            }
            self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode("utf-8"))
            self.wfile.flush()

        final_payload = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": requested_model or AUTO_MODEL_NAME,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        self.wfile.write(f"data: {json.dumps(final_payload)}\n\n".encode("utf-8"))
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()

    def log_message(self, format: str, *args) -> None:
        return


class RouterServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        handler: type[RouterHandler],
        index_file: Path,
        rag_runtime: RagRuntime | None = None,
    ) -> None:
        super().__init__(server_address, handler)
        self.index_file = index_file
        self.rag_runtime = rag_runtime

    def index_exists(self) -> bool:
        if self.rag_runtime is not None:
            return self.rag_runtime.index_file.exists()
        return self.index_file.exists()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local router service.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8788)
    parser.add_argument("--index-path", default=str(index_path()))
    args = parser.parse_args()

    index_file = Path(args.index_path).expanduser().resolve()
    server = RouterServer((args.host, args.port), RouterHandler, index_file)
    print(f"Router service listening on http://{args.host}:{args.port}")
    print(f"Index path: {index_file}")
    print(f"Auto model id: {AUTO_MODEL_NAME}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
