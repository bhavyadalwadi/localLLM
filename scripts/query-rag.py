#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from rag_lib import cosine_similarity, embed_text, index_path, load_json, top_k


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the local RAG index.")
    parser.add_argument("query", help="Query text.")
    parser.add_argument(
        "--index-path",
        default=str(index_path()),
        help="Path to the built RAG index.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=top_k(),
        help="Number of chunks to return.",
    )
    args = parser.parse_args()

    payload = load_json(Path(args.index_path).expanduser().resolve())
    items = payload.get("items", [])
    if not items:
        raise SystemExit("RAG index is empty. Build it first.")

    query_embedding = embed_text(args.query, payload.get("embedding_model"))
    ranked = []
    for item in items:
        ranked.append(
            {
                "score": cosine_similarity(query_embedding, item["embedding"]),
                "path": item["path"],
                "chunk_index": item["chunk_index"],
                "text": item["text"],
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    for item in ranked[: args.top_k]:
        print(f"SCORE: {item['score']:.4f}")
        print(f"SOURCE: {item['path']}#chunk-{item['chunk_index']}")
        print(item["text"])
        print("-" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
