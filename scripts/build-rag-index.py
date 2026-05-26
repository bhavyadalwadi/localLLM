#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from rag_lib import (
    documents_dir,
    embed_model,
    build_index_payload,
    build_existing_item_map,
    build_items,
    index_path,
    load_json,
    save_json,
)


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
