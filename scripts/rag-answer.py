#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from rag_lib import build_answer_prompt, chat_model, generate_text, index_path, load_json, rank_items, top_k


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

    ranked = rank_items(args.query, items, args.top_k, payload.get("embedding_model"))
    prompt = build_answer_prompt(args.query, ranked)
    answer = generate_text(prompt, args.model)
    print(answer)
    print("\nSources:")
    for item in ranked:
        print(f"- {item['path']}#chunk-{item['chunk_index']} ({item['score']:.4f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
