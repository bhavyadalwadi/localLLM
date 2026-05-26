#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

AUTO_BUILD_INDEX="${AUTO_BUILD_RAG_INDEX:-true}"
ROUTER_SERVICE_HOST="${ROUTER_SERVICE_HOST:-127.0.0.1}"
ROUTER_SERVICE_PORT="${ROUTER_SERVICE_PORT:-8788}"
RAG_CHAT_MODEL="${RAG_CHAT_MODEL:-gemma4:31b}"

exec python3 "${ROOT_DIR}/scripts/local_ai_runtime.py" \
  --host "${ROUTER_SERVICE_HOST}" \
  --port "${ROUTER_SERVICE_PORT}" \
  --documents-dir "${RAG_DOCUMENTS_DIR:-${ROOT_DIR}/rag-data/documents}" \
  --index-path "${RAG_INDEX_DIR:-${ROOT_DIR}/rag-data/chroma}/rag-index.json" \
  --model "${RAG_CHAT_MODEL}" \
  --auto-build-index "${AUTO_BUILD_INDEX}"
