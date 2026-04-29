#!/usr/bin/env bash

set -euo pipefail

# Run a simple preflight on a target Unix/Linux host before deployment.
# This validates command availability and basic directory layout assumptions.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

missing=0

check_command() {
  local name="$1"
  if command -v "${name}" >/dev/null 2>&1; then
    echo "OK: command '${name}' found"
  else
    echo "MISSING: command '${name}' not found"
    missing=1
  fi
}

echo "Running target host preflight ..."

check_command curl
check_command rsync
check_command docker

if [[ -n "${OLLAMA_BASE_URL:-}" ]]; then
  echo "INFO: OLLAMA_BASE_URL=${OLLAMA_BASE_URL}"
else
  echo "WARN: OLLAMA_BASE_URL is not set"
fi

if [[ -n "${BACKUP_ROOT_DIR:-}" ]]; then
  echo "INFO: BACKUP_ROOT_DIR=${BACKUP_ROOT_DIR}"
else
  echo "WARN: BACKUP_ROOT_DIR is not set"
fi

echo "Checking repo directories ..."
for dir in configs volumes rag-data backups scripts docs; do
  if [[ -d "${ROOT_DIR}/${dir}" ]]; then
    echo "OK: ${dir}/"
  else
    echo "MISSING: ${dir}/"
    missing=1
  fi
done

if [[ "${missing}" -ne 0 ]]; then
  echo "Preflight failed."
  exit 1
fi

echo "Preflight passed."

