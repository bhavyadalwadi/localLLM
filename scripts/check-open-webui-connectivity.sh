#!/usr/bin/env bash

set -euo pipefail

# Check that Open WebUI is reachable and that the Ollama API responds from the
# current execution context.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

OPEN_WEBUI_URL="${OPEN_WEBUI_URL:-http://localhost:3000}"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"
OLLAMA_CHECK_URL="${OLLAMA_CHECK_URL:-${OLLAMA_BASE_URL}}"

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is required."
  exit 1
fi

echo "Checking Open WebUI at ${OPEN_WEBUI_URL} ..."
curl -fsS "${OPEN_WEBUI_URL}/" >/dev/null

if [[ "${OLLAMA_CHECK_URL}" == *"host.docker.internal"* ]]; then
  OLLAMA_CHECK_URL="http://localhost:${OLLAMA_PORT:-11434}"
fi

echo "Checking Ollama at ${OLLAMA_CHECK_URL} ..."
curl -fsS "${OLLAMA_CHECK_URL}/api/tags" >/dev/null

echo "Open WebUI and Ollama are reachable."
