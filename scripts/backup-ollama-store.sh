#!/usr/bin/env bash

set -euo pipefail

# Back up the local Ollama model store to a configurable backup path.
# This can be a NAS mount, external disk, or another local directory.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

SOURCE_DIR="${OLLAMA_HOME_DIR:-$HOME/.ollama}"
BACKUP_ROOT="${BACKUP_ROOT_DIR:-/mnt/nas/local-ai-node/ollama-backups}"
TIMESTAMP="$(date +"%Y%m%d-%H%M%S")"
DEST_DIR="${BACKUP_ROOT}/ollama-home-${TIMESTAMP}"

if ! command -v rsync >/dev/null 2>&1; then
  echo "ERROR: rsync is required."
  exit 1
fi

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "ERROR: source directory does not exist: ${SOURCE_DIR}"
  exit 1
fi

mkdir -p "${DEST_DIR}"

echo "Backing up ${SOURCE_DIR} to ${DEST_DIR} ..."
rsync -a "${SOURCE_DIR}/" "${DEST_DIR}/"

echo "Backup complete: ${DEST_DIR}"

