#!/usr/bin/env bash

set -euo pipefail

# Check that Open WebUI is reachable and that the configured Ollama API responds.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

OPEN_WEBUI_URL="${OPEN_WEBUI_URL:-http://localhost:3000}"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is required."
  exit 1
fi

echo "Checking Open WebUI at ${OPEN_WEBUI_URL} ..."
curl -fsS "${OPEN_WEBUI_URL}/" >/dev/null

echo "Checking Ollama at ${OLLAMA_BASE_URL} ..."
curl -fsS "${OLLAMA_BASE_URL}/api/tags" >/dev/null

echo "Open WebUI and Ollama are reachable."

