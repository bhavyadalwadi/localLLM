#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

exec python3 "${ROOT_DIR}/scripts/idea_capture_service.py" \
  --host "${IDEA_CAPTURE_HOST:-127.0.0.1}" \
  --port "${IDEA_CAPTURE_PORT:-8790}" \
  --notes-dir "${IDEA_CAPTURE_NOTES_DIR:-${ROOT_DIR}/notes/idea-inbox}" \
  --model "${IDEA_CAPTURE_MODEL:-llama3.1:8b}"
