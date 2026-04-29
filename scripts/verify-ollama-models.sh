#!/usr/bin/env bash

set -euo pipefail

# Verify that the expected model inventory exists on the target node.
# This works against the Ollama HTTP API so it also supports Docker-only setups.
# Set RUN_SMOKE_TESTS=true to run lightweight prompt and embedding checks.

RUN_SMOKE_TESTS="${RUN_SMOKE_TESTS:-false}"
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"

required_models=(
  "llama3:8b"
  "deepseek-coder:6.7b"
  "nomic-embed-text"
  "phi3"
  "mixtral:8x7b"
  "llava:13b"
  "llama3:70b"
)

optional_models=(
  "gemma4:31b"
)

model_present() {
  local expected="$1"
  local installed

  for installed in "${installed_models[@]}"; do
    if [[ "${installed}" == "${expected}" ]]; then
      return 0
    fi

    if [[ "${expected}" != *:* && "${installed}" == "${expected}:latest" ]]; then
      return 0
    fi
  done

  return 1
}

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is required for API checks."
  exit 1
fi

echo "Checking Ollama API at ${OLLAMA_URL} ..."
tags_json="$(curl -fsS "${OLLAMA_URL}/api/tags")"

echo "Reading model inventory from the API ..."
installed_models=()
while IFS= read -r model; do
  installed_models+=("${model}")
done < <(printf '%s\n' "${tags_json}" | tr '{},' '\n' | sed -n 's/.*"model":"\([^"]*\)".*/\1/p')

missing_required=0

for model in "${required_models[@]}"; do
  if model_present "${model}"; then
    echo "OK: ${model}"
  else
    echo "MISSING: ${model}"
    missing_required=1
  fi
done

for model in "${optional_models[@]}"; do
  if model_present "${model}"; then
    echo "OPTIONAL OK: ${model}"
  else
    echo "OPTIONAL MISSING: ${model}"
  fi
done

if [[ "${RUN_SMOKE_TESTS}" == "true" ]]; then
  echo "Running smoke test for llama3:8b ..."
  curl -fsS "${OLLAMA_URL}/api/generate" \
    -H "Content-Type: application/json" \
    -d '{"model":"llama3:8b","prompt":"Reply with exactly: llama3 8b ready","stream":false}' >/dev/null

  echo "Running embedding smoke test for nomic-embed-text ..."
  curl -fsS "${OLLAMA_URL}/api/embeddings" \
    -H "Content-Type: application/json" \
    -d '{"model":"nomic-embed-text","prompt":"Local AI node test"}' >/dev/null
fi

if [[ "${missing_required}" -ne 0 ]]; then
  echo "Required model inventory is incomplete."
  exit 1
fi

echo "Ollama model inventory looks good."
