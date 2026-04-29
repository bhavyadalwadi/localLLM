# RAG Pipeline Placeholder

Status: not implemented.

Target direction:
- embeddings model: `nomic-embed-text`
- vector store: Chroma or FAISS
- document storage: `rag-data/documents/`
- persistence: `rag-data/chroma/` or `rag-data/faiss/`

Keep the first implementation simple:
- ingest local documents
- chunk text conservatively
- store embeddings locally
- expose retrieval through a small service or script layer

