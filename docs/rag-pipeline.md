# RAG Pipeline

This repo does not implement RAG yet, but the intended first version is now
defined enough to build against.

## First implementation target

- embeddings model: `nomic-embed-text`
- document source: `rag-data/documents/`
- vector store: Chroma first, FAISS as an alternative
- persistence: `rag-data/chroma/`
- retrieval consumer: Open WebUI or a small script/service layer

## Design rules

- Keep RAG separate from the base Ollama and Open WebUI deployment.
- Do not mix ingestion state into the live model store.
- Keep raw documents, chunks, and vector indexes in separate directories.
- Start with local documents only.

## Initial directory usage

- source documents: `rag-data/documents/`
- Chroma persistence: `rag-data/chroma/`
- FAISS experiments: `rag-data/faiss/`

## First-pass ingestion flow

1. Copy source material into `rag-data/documents/`.
2. Extract text into a normalized local representation.
3. Chunk conservatively to avoid losing context.
4. Generate embeddings with `nomic-embed-text`.
5. Write vectors to Chroma.
6. Expose retrieval to the UI or an agent layer.

## Model routing for RAG

Recommended split:
- embeddings: `nomic-embed-text`
- answer synthesis default: `llama3.1:8b`
- answer synthesis premium: `gemma4:31b`

Do not use the larger model for ingestion. Keep ingestion simple and stable.

## What not to do first

- do not add multiple vector stores at once
- do not mix cloud embeddings into the first local pipeline
- do not build agent orchestration before basic retrieval works
- do not let RAG change the required core-model inventory
