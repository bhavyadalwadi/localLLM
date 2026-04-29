#!/usr/bin/env bash

set -euo pipefail

# Download the Local AI Node model set onto any system with Ollama installed.
# Usage:
#   ./scripts/pull-required-models.sh
#
# Optional:
#   INCLUDE_OPTIONAL=true ./scripts/pull-required-models.sh

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

if [[ "${INCLUDE_OPTIONAL:-false}" == "true" ]]; then
  echo
  echo "Pulling optional models ..."
  for model in "${optional_models[@]}"; do
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

