#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

IDEA_CAPTURE_URL="${IDEA_CAPTURE_URL:-http://${IDEA_CAPTURE_HOST:-127.0.0.1}:${IDEA_CAPTURE_PORT:-8790}}"
IDEA_CAPTURE_SMOKE_TEST="${IDEA_CAPTURE_SMOKE_TEST:-false}"
TOKEN_HEADER=()

if [[ -n "${IDEA_CAPTURE_API_TOKEN:-}" ]]; then
  TOKEN_HEADER=(-H "Authorization: Bearer ${IDEA_CAPTURE_API_TOKEN}")
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is required."
  exit 1
fi

echo "Checking idea capture health at ${IDEA_CAPTURE_URL} ..."
health_json="$(curl -fsS "${TOKEN_HEADER[@]}" "${IDEA_CAPTURE_URL}/health")"

if [[ "${IDEA_CAPTURE_SMOKE_TEST}" == "true" ]]; then
  echo "Running idea capture smoke test ..."
  curl -fsS "${TOKEN_HEADER[@]}" "${IDEA_CAPTURE_URL}/capture" \
    -H "Content-Type: application/json" \
    -d '{"idea":"Half asleep idea about a better backup reminder flow.","source":"smoke-test"}' >/dev/null
fi

echo "Idea capture service is reachable."
printf '%s\n' "${health_json}" | sed -n 's/.*"model": "\([^"]*\)".*/Model: \1/p'
printf '%s\n' "${health_json}" | sed -n 's/.*"notes_dir": "\([^"]*\)".*/Notes dir: \1/p'
