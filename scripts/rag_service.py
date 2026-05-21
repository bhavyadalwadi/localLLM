#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from rag_lib import (
    build_answer_prompt,
    build_existing_item_map,
    build_index_payload,
    chunk_overlap,
    chunk_size,
    documents_dir,
    embed_model,
    embed_text,
    file_fingerprint,
    generate_text,
    index_path,
    iter_documents,
    load_json,
    read_text_file,
    rank_items,
    save_json,
    split_text,
    top_k,
)


def build_items(root: Path, existing_items: dict[tuple[str, str, int], dict] | None = None) -> list[dict]:
    items: list[dict] = []
    existing_items = existing_items or {}
    for path in iter_documents(root):
        text = read_text_file(path)
        chunks = split_text(text, chunk_size(), chunk_overlap())
        if not chunks:
            continue
        relative_path = path.relative_to(root)
        source_hash = file_fingerprint(path)
        for chunk_index, chunk_text in enumerate(chunks):
            existing_item = existing_items.get((str(relative_path), source_hash, chunk_index))
            if existing_item and existing_item.get("text") == chunk_text and isinstance(existing_item.get("embedding"), list):
                embedding = existing_item["embedding"]
            else:
                embedding = embed_text(chunk_text, embed_model())
            items.append(
                {
                    "id": f"{relative_path}#chunk-{chunk_index}",
                    "path": str(relative_path),
                    "chunk_index": chunk_index,
                    "source_hash": source_hash,
                    "text": chunk_text,
                    "embedding": embedding,
                }
            )
    return items


def rank_chunks(query: str, payload: dict, limit: int) -> list[dict]:
    return rank_items(query, payload.get("items", []), limit, payload.get("embedding_model"))


def answer_from_chunks(query: str, chunks: list[dict], model: str) -> str:
    prompt = build_answer_prompt(query, chunks)
    return generate_text(prompt, model)


class RagHandler(BaseHTTPRequestHandler):
    server: "RagServer"

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json(
                {
                    "ok": True,
                    "index_path": str(self.server.index_file),
                    "documents_dir": str(self.server.documents_root),
                }
            )
            return

        if self.path == "/index/status":
            payload = self.server.load_index()
            self.send_json(
                {
                    "items": len(payload.get("items", [])),
                    "embedding_model": payload.get("embedding_model"),
                    "chunk_size": payload.get("chunk_size"),
                    "chunk_overlap": payload.get("chunk_overlap"),
                }
            )
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        if self.path == "/index/build":
            payload = self.server.rebuild_index()
            self.send_json(
                {
                    "ok": True,
                    "items": len(payload.get("items", [])),
                    "index_path": str(self.server.index_file),
                }
            )
            return

        body = self.read_json()
        if self.path == "/query":
            query = body.get("query", "").strip()
            if not query:
                self.send_error(HTTPStatus.BAD_REQUEST, "query is required")
                return
            payload = self.server.load_index()
            limit = int(body.get("top_k", top_k()))
            chunks = rank_chunks(query, payload, limit)
            self.send_json({"query": query, "matches": chunks})
            return

        if self.path == "/answer":
            query = body.get("query", "").strip()
            if not query:
                self.send_error(HTTPStatus.BAD_REQUEST, "query is required")
                return
            payload = self.server.load_index()
            limit = int(body.get("top_k", top_k()))
            chunks = rank_chunks(query, payload, limit)
            model = body.get("model") or self.server.answer_model
            answer = answer_from_chunks(query, chunks, model)
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

    def log_message(self, format: str, *args) -> None:
        return


class RagServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], handler: type[RagHandler], documents_root: Path, index_file: Path, answer_model: str) -> None:
        super().__init__(server_address, handler)
        self.documents_root = documents_root
        self.index_file = index_file
        self.answer_model = answer_model

    def load_index(self) -> dict:
        if not self.index_file.exists():
            raise FileNotFoundError(f"Index not found: {self.index_file}")
        return load_json(self.index_file)

    def rebuild_index(self) -> dict:
        existing_items = {}
        if self.index_file.exists():
            existing_items = build_existing_item_map(load_json(self.index_file))
        items = build_items(self.documents_root, existing_items)
        payload = build_index_payload(items)
        save_json(self.index_file, payload)
        return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local RAG HTTP service.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--documents-dir", default=str(documents_dir()))
    parser.add_argument("--index-path", default=str(index_path()))
    parser.add_argument("--model", default="gemma4:31b")
    args = parser.parse_args()

    documents_root = Path(args.documents_dir).expanduser().resolve()
    index_file = Path(args.index_path).expanduser().resolve()

    server = RagServer((args.host, args.port), RagHandler, documents_root, index_file, args.model)
    print(f"RAG service listening on http://{args.host}:{args.port}")
    print(f"Documents directory: {documents_root}")
    print(f"Index path: {index_file}")
    print(f"Answer model: {args.model}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
