#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import os
import time
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


def build_index_payload(items: list[dict]) -> dict:
    return {
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "documents_dir": str(documents_dir()),
        "embedding_model": embed_model(),
        "chunk_size": chunk_size(),
        "chunk_overlap": chunk_overlap(),
        "items": items,
    }
