#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from rag_lib import (
    build_index_payload,
    chunk_overlap,
    chunk_size,
    documents_dir,
    embed_model,
    embed_text,
    index_path,
    iter_documents,
    read_text_file,
    save_json,
    split_text,
)


def build_items(root: Path) -> list[dict]:
    items: list[dict] = []
    for path in iter_documents(root):
        text = read_text_file(path)
        chunks = split_text(text, chunk_size(), chunk_overlap())
        if not chunks:
            continue

        relative_path = path.relative_to(root)
        for chunk_index, chunk_text in enumerate(chunks):
            embedding = embed_text(chunk_text, embed_model())
            items.append(
                {
                    "id": f"{relative_path}#chunk-{chunk_index}",
                    "path": str(relative_path),
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                    "embedding": embedding,
                }
            )
    return items


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

    items = build_items(source_dir)
    payload = build_index_payload(items)
    save_json(output_path, payload)

    print(f"Wrote {len(items)} chunks to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
