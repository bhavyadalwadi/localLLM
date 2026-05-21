#!/usr/bin/env bash

set -euo pipefail

# Convenience wrapper for the common Local AI Node setup and validation flow.
# The primary operator path remains preflight, pull/restore, verify, then start
# services directly with the smaller scripts in this repo.
# Usage examples:
#   ./scripts/bootstrap-local-ai-node.sh
#   OPTIONAL_MODELS="gemma4:31b,llava:13b" ./scripts/bootstrap-local-ai-node.sh
#   OPTIONAL_MODELS="gemma4:31b,llava:13b" RUN_SMOKE_TESTS=true ./scripts/bootstrap-local-ai-node.sh
#   ./scripts/bootstrap-local-ai-node.sh --docker-ollama
#   ./scripts/bootstrap-local-ai-node.sh --pull
#   ./scripts/bootstrap-local-ai-node.sh --restore /path/to/ollama-backup

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

PULL_MODELS="${PULL_MODELS:-false}"
RUN_SMOKE_TESTS="${RUN_SMOKE_TESTS:-false}"
START_DOCKER="${START_DOCKER:-true}"
USE_DOCKER_OLLAMA="${USE_DOCKER_OLLAMA:-false}"
RESTORE_FROM="${RESTORE_FROM:-}"
OPTIONAL_MODELS="${OPTIONAL_MODELS:-}"
EXPECT_OPTIONAL_MODELS="${EXPECT_OPTIONAL_MODELS:-}"

usage() {
  cat <<'EOF'
Usage: ./scripts/bootstrap-local-ai-node.sh [options]

Convenience wrapper around:
  ./scripts/preflight-target-host.sh
  ./scripts/pull-required-models.sh
  ./scripts/verify-ollama-models.sh
  docker compose up -d

Options:
  --pull                Pull the required model set before validation.
  --restore PATH        Restore an Ollama store backup before validation.
  --docker-ollama       Start Open WebUI and Ollama in Docker Compose.
  --skip-docker         Skip docker compose startup.
  --smoke-tests         Run lightweight generation and embedding smoke tests.
  --help                Show this help text.

Environment overrides:
  OPTIONAL_MODELS="gemma4:31b,llava:13b"
  EXPECT_OPTIONAL_MODELS="gemma4:31b,llava:13b"
  ENV_FILE=/path/to/.env
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pull)
      PULL_MODELS="true"
      shift
      ;;
    --restore)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --restore requires a path."
        exit 1
      fi
      RESTORE_FROM="$2"
      shift 2
      ;;
    --docker-ollama)
      USE_DOCKER_OLLAMA="true"
      shift
      ;;
    --skip-docker)
      START_DOCKER="false"
      shift
      ;;
    --smoke-tests)
      RUN_SMOKE_TESTS="true"
      shift
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "ERROR: .env not found at ${ENV_FILE}"
  echo "Create it from .env.example or .env.staging.example first."
  exit 1
fi

if [[ -n "${OPTIONAL_MODELS}" && -z "${EXPECT_OPTIONAL_MODELS}" ]]; then
  EXPECT_OPTIONAL_MODELS="${OPTIONAL_MODELS}"
fi

echo "Using environment file: ${ENV_FILE}"
echo "Running preflight ..."
"${ROOT_DIR}/scripts/preflight-target-host.sh"

if [[ -n "${RESTORE_FROM}" ]]; then
  echo
  echo "Restoring Ollama store from ${RESTORE_FROM} ..."
  CONFIRM_RESTORE=true "${ROOT_DIR}/scripts/restore-ollama-store.sh" "${RESTORE_FROM}"
fi

if [[ "${PULL_MODELS}" == "true" ]]; then
  echo
  echo "Pulling model inventory ..."
  if [[ -n "${OPTIONAL_MODELS}" ]]; then
    OPTIONAL_MODELS="${OPTIONAL_MODELS}" "${ROOT_DIR}/scripts/pull-required-models.sh"
  else
    "${ROOT_DIR}/scripts/pull-required-models.sh"
  fi
fi

echo
echo "Verifying model inventory ..."
if [[ -n "${EXPECT_OPTIONAL_MODELS}" ]]; then
  EXPECT_OPTIONAL_MODELS="${EXPECT_OPTIONAL_MODELS}" "${ROOT_DIR}/scripts/verify-ollama-models.sh"
else
  "${ROOT_DIR}/scripts/verify-ollama-models.sh"
fi

if [[ "${START_DOCKER}" == "true" ]]; then
  echo
  echo "Starting Docker services ..."
  if [[ "${USE_DOCKER_OLLAMA}" == "true" ]]; then
    (
      cd "${ROOT_DIR}"
      docker compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
    )
  else
    (
      cd "${ROOT_DIR}"
      docker compose up -d
    )
  fi

  echo
  echo "Checking service connectivity ..."
  "${ROOT_DIR}/scripts/check-open-webui-connectivity.sh"
fi

if [[ "${RUN_SMOKE_TESTS}" == "true" ]]; then
  echo
  echo "Running smoke tests ..."
  RUN_SMOKE_TESTS=true "${ROOT_DIR}/scripts/verify-ollama-models.sh"
fi

echo
echo "Bootstrap complete."
