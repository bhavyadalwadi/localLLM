#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from rag_lib import chat_model, cosine_similarity, embed_text, generate_text, index_path, load_json, top_k


def main() -> int:
    parser = argparse.ArgumentParser(description="Answer a question using local RAG.")
    parser.add_argument("query", help="Question to answer.")
    parser.add_argument(
        "--index-path",
        default=str(index_path()),
        help="Path to the built RAG index.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=top_k(),
        help="Number of chunks to include as context.",
    )
    parser.add_argument(
        "--model",
        default=chat_model(),
        help="Generation model to use for the final answer.",
    )
    args = parser.parse_args()

    payload = load_json(Path(args.index_path).expanduser().resolve())
    items = payload.get("items", [])
    if not items:
        raise SystemExit("RAG index is empty. Build it first.")

    query_embedding = embed_text(args.query, payload.get("embedding_model"))
    ranked = sorted(
        (
            {
                "score": cosine_similarity(query_embedding, item["embedding"]),
                "path": item["path"],
                "chunk_index": item["chunk_index"],
                "text": item["text"],
            }
            for item in items
        ),
        key=lambda item: item["score"],
        reverse=True,
    )[: args.top_k]

    context_sections = []
    for item in ranked:
        context_sections.append(
            f"[Source: {item['path']}#chunk-{item['chunk_index']} score={item['score']:.4f}]\n{item['text']}"
        )

    prompt = (
        "Answer the user's question using only the provided context. "
        "If the context is insufficient, say so clearly.\n\n"
        f"Question:\n{args.query}\n\n"
        "Context:\n"
        f"{'\n\n'.join(context_sections)}\n\n"
        "Answer:"
    )

    answer = generate_text(prompt, args.model)
    print(answer)
    print("\nSources:")
    for item in ranked:
        print(f"- {item['path']}#chunk-{item['chunk_index']} ({item['score']:.4f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
