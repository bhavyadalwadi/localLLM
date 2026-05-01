#!/usr/bin/env bash

set -euo pipefail

# Show the manifest and blob files required for a specific Ollama model.
# Usage:
#   ./scripts/show-model-files.sh gemma4:31b
#   ./scripts/show-model-files.sh llava:13b

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <model[:tag]>"
  exit 1
fi

model_ref="$1"
model_name="${model_ref%%:*}"
model_tag="${model_ref#*:}"

if [[ "${model_name}" == "${model_tag}" ]]; then
  model_tag="latest"
fi

manifest_root="${OLLAMA_MANIFEST_ROOT:-${HOME}/.ollama/models/manifests/registry.ollama.ai/library}"
blob_root="${OLLAMA_BLOB_ROOT:-${HOME}/.ollama/models/blobs}"
manifest_path="${manifest_root}/${model_name}/${model_tag}"

if [[ ! -f "${manifest_path}" ]]; then
  echo "ERROR: manifest not found for ${model_name}:${model_tag}"
  echo "Expected: ${manifest_path}"
  exit 1
fi

manifest_size="$(wc -c < "${manifest_path}" | tr -d '[:space:]')"

echo "Model: ${model_name}:${model_tag}"
echo "Manifest: ${manifest_path}"
echo "Manifest size: ${manifest_size} bytes"
echo
echo "Required files:"
echo "${manifest_path}"

while IFS= read -r digest; do
  [[ -n "${digest}" ]] || continue

  blob_file="${blob_root}/${digest/:/-}"
  if [[ -f "${blob_file}" ]]; then
    blob_size="$(wc -c < "${blob_file}" | tr -d '[:space:]')"
    echo "${blob_file} (${blob_size} bytes)"
  else
    echo "${blob_file} (MISSING)"
  fi
done < <(
  grep -o '"digest":"sha256:[^"]*"' "${manifest_path}" \
    | sed 's/"digest":"\(sha256:[^"]*\)"/\1/' \
    | awk '!seen[$0]++'
)
