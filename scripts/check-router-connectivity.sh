#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

ROUTER_URL="${ROUTER_URL:-http://${ROUTER_SERVICE_HOST:-127.0.0.1}:${ROUTER_SERVICE_PORT:-8788}}"
RUN_SMOKE_TESTS="${RUN_SMOKE_TESTS:-false}"

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is required."
  exit 1
fi

echo "Checking router health at ${ROUTER_URL} ..."
health_json="$(curl -fsS "${ROUTER_URL}/health")"

echo "Checking router model list ..."
models_json="$(curl -fsS "${ROUTER_URL}/v1/models")"

if ! printf '%s\n' "${models_json}" | grep -q '"id": "local-ai-node-auto"'; then
  echo "ERROR: local-ai-node-auto is missing from router model list."
  exit 1
fi

if [[ "${RUN_SMOKE_TESTS}" == "true" ]]; then
  echo "Running router smoke test ..."
  curl -fsS "${ROUTER_URL}/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d '{
      "model":"local-ai-node-auto",
      "messages":[
        {"role":"user","content":"Reply with exactly: router ready"}
      ],
      "stream":false
    }' >/dev/null
fi

echo "Router is reachable."
printf '%s\n' "${health_json}" | sed -n 's/.*"default_model": "\([^"]*\)".*/Default model: \1/p'
printf '%s\n' "${health_json}" | sed -n 's/.*"code_model": "\([^"]*\)".*/Code model: \1/p'
printf '%s\n' "${health_json}" | sed -n 's/.*"light_model": "\([^"]*\)".*/Light model: \1/p'
printf '%s\n' "${health_json}" | sed -n 's/.*"rag_model": "\([^"]*\)".*/RAG model: \1/p'
