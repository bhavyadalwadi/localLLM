# RAG Pipeline

This repo now includes a first-pass local RAG implementation built around
Ollama embeddings, a dependency-light JSON index, and a small local HTTP
service.

## Current implementation

- embeddings model: `nomic-embed-text`
- source documents: `rag-data/documents/`
- local index file: `rag-data/chroma/rag-index.json`
- retrieval scripts:
  - `scripts/build-rag-index.py`
  - `scripts/query-rag.py`
  - `scripts/rag-answer.py`
  - `scripts/rag_service.py`
  - `scripts/start-rag-service.sh`

This is intentionally simple. It creates a local disk index that is easy to
inspect, back up, and rebuild without introducing new service dependencies.
Ranking is hybrid: embeddings first, then a light lexical boost from filenames
and chunk text so obvious deployment or security questions map to the right docs
more reliably.

## Build the index

Place source material under `rag-data/documents/`, then run:

```bash
python3 ./scripts/build-rag-index.py
```

Useful overrides:

```bash
RAG_DOCUMENTS_DIR=docs python3 ./scripts/build-rag-index.py
RAG_CHUNK_SIZE=1500 RAG_CHUNK_OVERLAP=250 python3 ./scripts/build-rag-index.py
```

## Query the index

Inspect the top matching chunks:

```bash
python3 ./scripts/query-rag.py "How is this node supposed to be deployed?"
```

Generate an answer using retrieved context:

```bash
python3 ./scripts/rag-answer.py "What are the default model roles?"
```

Use a larger answer model when needed:

```bash
RAG_CHAT_MODEL=gemma4:31b python3 ./scripts/rag-answer.py "Summarize the security posture."
```

## Run the local RAG service

Start the HTTP service:

```bash
./scripts/start-rag-service.sh
```

Health check:

```bash
curl http://127.0.0.1:8787/health
```

Build the index through the service:

```bash
curl -X POST http://127.0.0.1:8787/index/build
```

Query retrieved chunks:

```bash
curl -X POST http://127.0.0.1:8787/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the deployment flow for this node?","top_k":4}'
```

Generate a grounded answer:

```bash
curl -X POST http://127.0.0.1:8787/answer \
  -H "Content-Type: application/json" \
  -d '{"query":"What models are part of the core stack?","top_k":4,"model":"gemma4:31b"}'
```

## Design rules

- Keep RAG separate from the base Ollama and Open WebUI deployment.
- Do not mix ingestion state into the live model store.
- Keep raw documents in `rag-data/documents/`.
- Keep generated index state in `rag-data/chroma/`.
- Start with local text documents only.

## Model routing for RAG

Recommended split:
- embeddings: `nomic-embed-text`
- answer synthesis default: `llama3.1:8b`
- answer synthesis premium: `gemma4:31b`

Do not use the larger model for ingestion. Keep ingestion simple and stable.

## Next step after this baseline

Once this local JSON index is working for your documents, the next upgrade path
is:

1. swap the index backend to Chroma
2. integrate the local service into the UI or agent workflows
3. add metadata filters and incremental reindexing
