#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

RAG_SERVICE_HOST="${RAG_SERVICE_HOST:-127.0.0.1}"
RAG_SERVICE_PORT="${RAG_SERVICE_PORT:-8787}"
RAG_CHAT_MODEL="${RAG_CHAT_MODEL:-gemma4:31b}"

exec python3 "${ROOT_DIR}/scripts/rag_service.py" \
  --host "${RAG_SERVICE_HOST}" \
  --port "${RAG_SERVICE_PORT}" \
  --documents-dir "${RAG_DOCUMENTS_DIR:-${ROOT_DIR}/rag-data/documents}" \
  --index-path "${RAG_INDEX_DIR:-${ROOT_DIR}/rag-data/chroma}/rag-index.json" \
  --model "${RAG_CHAT_MODEL}"
