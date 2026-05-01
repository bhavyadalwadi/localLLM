#!/usr/bin/env bash

set -euo pipefail

# Download the Local AI Node model set onto any system with Ollama installed.
# Usage:
#   ./scripts/pull-required-models.sh
#
# Optional:
#   INCLUDE_OPTIONAL=true ./scripts/pull-required-models.sh
#   OPTIONAL_MODELS="gemma4:31b" ./scripts/pull-required-models.sh
#   OPTIONAL_MODELS="llava:13b,qwen3:30b" ./scripts/pull-required-models.sh

required_models=(
  "llama3.1:8b"
  "deepseek-coder:6.7b"
  "nomic-embed-text"
  "phi3"
)

optional_models=(
  "llava:13b"
  "gemma4:31b"
  "qwen3:30b"
)

if ! command -v ollama >/dev/null 2>&1; then
  echo "ERROR: ollama is not installed or not in PATH."
  exit 1
fi

echo "Checking Ollama availability ..."
ollama --version >/dev/null

echo "Pulling required models ..."
for model in "${required_models[@]}"; do
  echo
  echo "==> Pulling ${model}"
  ollama pull "${model}"
done

selected_optional_models=()
if [[ -n "${OPTIONAL_MODELS:-}" ]]; then
  IFS=',' read -r -a selected_optional_models <<<"${OPTIONAL_MODELS}"
elif [[ "${INCLUDE_OPTIONAL:-false}" == "true" ]]; then
  selected_optional_models=("${optional_models[@]}")
fi

if [[ "${#selected_optional_models[@]}" -gt 0 ]]; then
  echo
  echo "Pulling optional models ..."
  for model in "${selected_optional_models[@]}"; do
    echo
    echo "==> Pulling ${model}"
    ollama pull "${model}"
  done
fi

echo
echo "Final model inventory:"
ollama list

echo
echo "Done."
