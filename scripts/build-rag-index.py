#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from rag_lib import (
    build_existing_item_map,
    build_index_payload,
    chunk_overlap,
    chunk_size,
    documents_dir,
    embed_model,
    embed_text,
    file_fingerprint,
    index_path,
    iter_documents,
    load_json,
    read_text_file,
    save_json,
    split_text,
)


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the local RAG index.")
    parser.add_argument(
        "--documents-dir",
        default=str(documents_dir()),
        help="Directory of source documents to ingest.",
    )
    parser.add_argument(
        "--index-path",
        default=str(index_path()),
        help="Output JSON index path.",
    )
    args = parser.parse_args()

    source_dir = Path(args.documents_dir).expanduser().resolve()
    output_path = Path(args.index_path).expanduser().resolve()

    if not source_dir.is_dir():
        raise SystemExit(f"Documents directory not found: {source_dir}")

    print(f"Building RAG index from {source_dir}")
    print(f"Embedding model: {embed_model()}")

    existing_items = {}
    if output_path.exists():
        existing_items = build_existing_item_map(load_json(output_path))

    items, reused_chunks = build_items(source_dir, existing_items)
    payload = build_index_payload(items)
    save_json(output_path, payload)

    print(f"Wrote {len(items)} chunks to {output_path}")
    print(f"Reused {reused_chunks} unchanged chunks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
