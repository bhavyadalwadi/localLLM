#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from pathlib import Path

from rag_lib import RagRuntime, documents_dir, index_path, top_k
from router_service import (
    AUTO_MODEL_NAME,
    RouterHandler,
    RouterServer,
    code_model,
    default_model,
    light_model,
    openai_chat_response,
    rag_model,
    vision_model,
    build_chat_result,
)


class LocalAIRuntimeHandler(RouterHandler):
    server: "LocalAIRuntimeServer"

    def do_GET(self) -> None:
        if self.path == "/health":
            index_status = self.server.index_status_payload()
            self.send_json(
                {
                    "ok": True,
                    "service": "local-ai-runtime",
                    "index": index_status,
                    "default_model": default_model(),
                    "code_model": code_model(),
                    "light_model": light_model(),
                    "rag_model": rag_model(),
                    "vision_model": vision_model(),
                }
            )
            return

        if self.path == "/index/status":
            self.send_json(self.server.index_status_payload())
            return

        super().do_GET()

    def do_POST(self) -> None:
        if self.path == "/index/rebuild":
            payload = self.server.rag_runtime.rebuild_index()
            self.send_json(
                {
                    "ok": True,
                    "items": len(payload.get("items", [])),
                    "index_path": str(self.server.rag_runtime.index_file),
                }
            )
            return

        if self.path == "/query":
            body = self.read_json()
            query = str(body.get("query", "")).strip()
            if not query:
                self.send_error(HTTPStatus.BAD_REQUEST, "query is required")
                return
            limit = int(body.get("top_k", top_k()))
            matches = self.server.rag_runtime.query(query, limit)
            self.send_json({"query": query, "matches": matches})
            return

        if self.path == "/answer":
            body = self.read_json()
            query = str(body.get("query", "")).strip()
            if not query:
                self.send_error(HTTPStatus.BAD_REQUEST, "query is required")
                return
            limit = int(body.get("top_k", top_k()))
            model = body.get("model") or self.server.rag_runtime.answer_model
            answer, chunks = self.server.rag_runtime.answer(query, model=model, limit=limit)
            self.send_json(
                {
                    "query": query,
                    "model": model,
                    "answer": answer,
                    "sources": [
                        {
                            "path": item["path"],
                            "chunk_index": item["chunk_index"],
                            "score": item["score"],
                        }
                        for item in chunks
                    ],
                }
            )
            return

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


class LocalAIRuntimeServer(RouterServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        index_file: Path,
        rag_runtime: RagRuntime,
    ) -> None:
        super().__init__(server_address, LocalAIRuntimeHandler, index_file, rag_runtime=rag_runtime)
        self.rag_runtime = rag_runtime

    def index_status_payload(self) -> dict:
        try:
            status = self.rag_runtime.status()
            return {"ready": True, **status}
        except FileNotFoundError:
            return {
                "ready": False,
                "index_path": str(self.rag_runtime.index_file),
                "documents_dir": str(self.rag_runtime.documents_root),
            }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the single-process local AI runtime.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8788)
    parser.add_argument("--documents-dir", default=str(documents_dir()))
    parser.add_argument("--index-path", default=str(index_path()))
    parser.add_argument("--model", default=rag_model())
    parser.add_argument("--auto-build-index", choices=("true", "false"), default="true")
    args = parser.parse_args()

    documents_root = Path(args.documents_dir).expanduser().resolve()
    index_file = Path(args.index_path).expanduser().resolve()
    rag_runtime = RagRuntime(documents_root, index_file, args.model)
    rag_runtime.ensure_index(auto_build=args.auto_build_index == "true")

    server = LocalAIRuntimeServer((args.host, args.port), index_file, rag_runtime)
    print(f"Local AI runtime listening on http://{args.host}:{args.port}")
    print(f"Documents directory: {documents_root}")
    print(f"Index path: {index_file}")
    print(f"Auto model id: {AUTO_MODEL_NAME}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
