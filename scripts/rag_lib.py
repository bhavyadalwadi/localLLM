#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import os
import re
import time
import base64
import hashlib
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable


TEXT_EXTENSIONS = {
    ".c",
    ".cpp",
    ".css",
    ".csv",
    ".go",
    ".h",
    ".hpp",
    ".html",
    ".java",
    ".js",
    ".json",
    ".log",
    ".md",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".text",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


def env_path(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default)).expanduser().resolve()


def ollama_url() -> str:
    return os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")


def embed_model() -> str:
    return os.environ.get("RAG_EMBED_MODEL", "nomic-embed-text")


def chat_model() -> str:
    return os.environ.get("RAG_CHAT_MODEL", "llama3.1:8b")


def documents_dir() -> Path:
    return env_path("RAG_DOCUMENTS_DIR", "rag-data/documents")


def index_dir() -> Path:
    return env_path("RAG_INDEX_DIR", "rag-data/chroma")


def index_path() -> Path:
    return index_dir() / "rag-index.json"


def chunk_size() -> int:
    return int(os.environ.get("RAG_CHUNK_SIZE", "1200"))


def chunk_overlap() -> int:
    return int(os.environ.get("RAG_CHUNK_OVERLAP", "200"))


def top_k() -> int:
    return int(os.environ.get("RAG_TOP_K", "4"))


def max_file_bytes() -> int:
    return int(os.environ.get("RAG_MAX_FILE_BYTES", str(2 * 1024 * 1024)))


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach {url}: {exc.reason}") from exc


def embed_text(text: str, model: str | None = None) -> list[float]:
    payload = {"model": model or embed_model(), "prompt": text}
    response = post_json(f"{ollama_url()}/api/embeddings", payload)
    vector = response.get("embedding")
    if not isinstance(vector, list):
        raise RuntimeError("Embedding response did not include an embedding vector.")
    return [float(value) for value in vector]


def generate_text(prompt: str, model: str | None = None) -> str:
    payload = {"model": model or chat_model(), "prompt": prompt, "stream": False}
    response = post_json(f"{ollama_url()}/api/generate", payload)
    output = response.get("response")
    if not isinstance(output, str):
        raise RuntimeError("Generation response did not include text.")
    return output.strip()


def normalize_image_input(image_ref: str) -> str:
    if image_ref.startswith("data:"):
        _, _, encoded = image_ref.partition(",")
        if not encoded:
            raise RuntimeError("Image data URL did not include encoded content.")
        return encoded.strip()

    if image_ref.startswith(("http://", "https://")):
        try:
            with urllib.request.urlopen(image_ref) as response:
                return base64.b64encode(response.read()).decode("utf-8")
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Could not fetch image URL {image_ref}: {exc.reason}") from exc

    path = Path(image_ref.replace("file://", "", 1)).expanduser()
    if not path.exists():
        raise RuntimeError(f"Image path does not exist: {image_ref}")
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def generate_text_with_images(prompt: str, images: list[str], model: str | None = None) -> str:
    payload = {
        "model": model or chat_model(),
        "prompt": prompt,
        "images": [normalize_image_input(image) for image in images],
        "stream": False,
    }
    response = post_json(f"{ollama_url()}/api/generate", payload)
    output = response.get("response")
    if not isinstance(output, str):
        raise RuntimeError("Generation response did not include text.")
    return output.strip()


def iter_documents(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if path.stat().st_size > max_file_bytes():
            continue
        yield path


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def file_fingerprint(path: Path) -> str:
    stat = path.stat()
    payload = f"{path.resolve()}::{stat.st_mtime_ns}::{stat.st_size}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def split_text(text: str, size: int, overlap: int) -> list[str]:
    normalized = "\n".join(line.rstrip() for line in text.splitlines())
    normalized = normalized.strip()
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(len(normalized), start + size)
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(normalized):
            break
        start = max(end - overlap, start + 1)
    return chunks


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return numerator / (left_norm * right_norm)


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def lexical_overlap_score(query: str, path: str, text: str) -> float:
    query_tokens = set(tokenize(query))
    if not query_tokens:
        return 0.0

    path_tokens = set(tokenize(path.replace("/", " ")))
    text_tokens = set(tokenize(text[:2000]))
    path_overlap = len(query_tokens & path_tokens) / len(query_tokens)
    text_overlap = len(query_tokens & text_tokens) / len(query_tokens)
    return (path_overlap * 1.5) + text_overlap


def rank_items(query: str, items: list[dict], limit: int, embedding_model: str | None = None) -> list[dict]:
    query_embedding = embed_text(query, embedding_model)
    ranked = []
    for item in items:
        semantic_score = cosine_similarity(query_embedding, item["embedding"])
        lexical_score = lexical_overlap_score(query, item["path"], item["text"])
        final_score = semantic_score + (lexical_score * 0.15)
        ranked.append(
            {
                "score": final_score,
                "semantic_score": semantic_score,
                "lexical_score": lexical_score,
                "path": item["path"],
                "chunk_index": item["chunk_index"],
                "text": item["text"],
            }
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:limit]


def build_answer_prompt(query: str, chunks: list[dict]) -> str:
    context_sections = [
        (
            f"[Source: {item['path']}#chunk-{item['chunk_index']} "
            f"score={item['score']:.4f} semantic={item['semantic_score']:.4f} "
            f"lexical={item['lexical_score']:.4f}]\n{item['text']}"
        )
        for item in chunks
    ]
    return (
        "You are answering from a local knowledge base. "
        "Use only the provided context. "
        "Give a direct, useful answer with 2-5 concrete points when possible. "
        "Do not answer with a vague one-line label if the context supports more detail. "
        "If the context is insufficient, say exactly what is missing. "
        "End with a short 'Sources:' line listing the most relevant file names.\n\n"
        f"Question:\n{query}\n\n"
        "Context:\n"
        f"{'\n\n'.join(context_sections)}\n\n"
        "Answer:"
    )


def build_index_payload(items: list[dict]) -> dict:
    return {
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "documents_dir": str(documents_dir()),
        "embedding_model": embed_model(),
        "chunk_size": chunk_size(),
        "chunk_overlap": chunk_overlap(),
        "items": items,
    }


def index_settings_match(payload: dict) -> bool:
    return (
        payload.get("embedding_model") == embed_model()
        and payload.get("chunk_size") == chunk_size()
        and payload.get("chunk_overlap") == chunk_overlap()
    )


def build_existing_item_map(payload: dict) -> dict[tuple[str, str, int], dict]:
    existing: dict[tuple[str, str, int], dict] = {}
    if not index_settings_match(payload):
        return existing

    for item in payload.get("items", []):
        source_hash = item.get("source_hash")
        path = item.get("path")
        chunk_index = item.get("chunk_index")
        if not isinstance(source_hash, str) or not isinstance(path, str) or not isinstance(chunk_index, int):
            continue
        existing[(path, source_hash, chunk_index)] = item
    return existing


def build_items(root: Path, existing_items: dict[tuple[str, str, int], dict] | None = None) -> tuple[list[dict], int]:
    items: list[dict] = []
    reused_chunks = 0
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
                reused_chunks += 1
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
    return items, reused_chunks


class RagRuntime:
    def __init__(self, documents_root: Path, index_file: Path, answer_model: str) -> None:
        self.documents_root = documents_root
        self.index_file = index_file
        self.answer_model = answer_model

    def load_index(self) -> dict:
        if not self.index_file.exists():
            raise FileNotFoundError(f"Index not found: {self.index_file}")
        return load_json(self.index_file)

    def rebuild_index(self) -> dict:
        if not self.documents_root.is_dir():
            raise FileNotFoundError(f"Documents directory not found: {self.documents_root}")

        existing_items = {}
        if self.index_file.exists():
            existing_items = build_existing_item_map(load_json(self.index_file))

        items, _ = build_items(self.documents_root, existing_items)
        payload = build_index_payload(items)
        save_json(self.index_file, payload)
        return payload

    def ensure_index(self, auto_build: bool) -> dict | None:
        if self.index_file.exists():
            return self.load_index()
        if not auto_build:
            return None
        return self.rebuild_index()

    def status(self) -> dict:
        payload = self.load_index()
        return {
            "items": len(payload.get("items", [])),
            "embedding_model": payload.get("embedding_model"),
            "chunk_size": payload.get("chunk_size"),
            "chunk_overlap": payload.get("chunk_overlap"),
            "index_path": str(self.index_file),
            "documents_dir": str(self.documents_root),
        }

    def query(self, query: str, limit: int) -> list[dict]:
        payload = self.load_index()
        return rank_items(query, payload.get("items", []), limit, payload.get("embedding_model"))

    def answer(self, query: str, model: str | None = None, limit: int | None = None) -> tuple[str, list[dict]]:
        chunks = self.query(query, limit or top_k())
        prompt = build_answer_prompt(query, chunks)
        return generate_text(prompt, model or self.answer_model), chunks
