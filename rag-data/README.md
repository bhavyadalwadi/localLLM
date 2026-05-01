# RAG Data

Current layout:
- `documents/` for source files to ingest
- `chroma/` for the first-pass local JSON index and later Chroma persistence
- `faiss/` reserved for later FAISS experiments

Build the current local index with:

```bash
python3 ./scripts/build-rag-index.py
```
