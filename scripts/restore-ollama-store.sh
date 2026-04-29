#!/usr/bin/env bash

set -euo pipefail

# Restore a backup into the local Ollama model store.
# Usage:
#   CONFIRM_RESTORE=true ./scripts/restore-ollama-store.sh /path/to/backup

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

if [[ "${CONFIRM_RESTORE:-false}" != "true" ]]; then
  echo "ERROR: set CONFIRM_RESTORE=true to proceed."
  exit 1
fi

if [[ $# -ne 1 ]]; then
  echo "Usage: CONFIRM_RESTORE=true $0 /path/to/backup"
  exit 1
fi

BACKUP_SOURCE="$1"
TARGET_DIR="${OLLAMA_HOME_DIR:-$HOME/.ollama}"
SAFETY_BACKUP="${TARGET_DIR}.pre-restore-$(date +"%Y%m%d-%H%M%S")"

if ! command -v rsync >/dev/null 2>&1; then
  echo "ERROR: rsync is required."
  exit 1
fi

if [[ ! -d "${BACKUP_SOURCE}" ]]; then
  echo "ERROR: backup source does not exist: ${BACKUP_SOURCE}"
  exit 1
fi

if [[ -d "${TARGET_DIR}" ]]; then
  echo "Creating safety backup at ${SAFETY_BACKUP} ..."
  rsync -a "${TARGET_DIR}/" "${SAFETY_BACKUP}/"
fi

mkdir -p "${TARGET_DIR}"

echo "Restoring ${BACKUP_SOURCE} into ${TARGET_DIR} ..."
rsync -a "${BACKUP_SOURCE}/" "${TARGET_DIR}/"

echo "Restore complete."

