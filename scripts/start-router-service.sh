#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

ROUTER_SERVICE_HOST="${ROUTER_SERVICE_HOST:-127.0.0.1}"
ROUTER_SERVICE_PORT="${ROUTER_SERVICE_PORT:-8788}"

exec python3 "${ROOT_DIR}/scripts/router_service.py" \
  --host "${ROUTER_SERVICE_HOST}" \
  --port "${ROUTER_SERVICE_PORT}" \
  --index-path "${RAG_INDEX_DIR:-${ROOT_DIR}/rag-data/chroma}/rag-index.json"
