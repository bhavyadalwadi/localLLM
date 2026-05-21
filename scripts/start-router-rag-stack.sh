#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env}"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

RAG_INDEX_PATH="${RAG_INDEX_DIR:-${ROOT_DIR}/rag-data/chroma}/rag-index.json"
RUN_DIR="${RAG_RUN_DIR:-${ROOT_DIR}/rag-data/run}"
LOG_DIR="${RAG_LOG_DIR:-${ROOT_DIR}/rag-data/logs}"
PID_FILE="${RUN_DIR}/rag-service.pid"
LOG_FILE="${LOG_DIR}/rag-service.log"
AUTO_BUILD_INDEX="${AUTO_BUILD_RAG_INDEX:-true}"
STARTED_RAG="false"

mkdir -p "${RUN_DIR}" "${LOG_DIR}"

cleanup() {
  if [[ "${STARTED_RAG}" == "true" && -f "${PID_FILE}" ]]; then
    rag_pid="$(cat "${PID_FILE}")"
    if kill -0 "${rag_pid}" >/dev/null 2>&1; then
      kill "${rag_pid}" >/dev/null 2>&1 || true
    fi
    rm -f "${PID_FILE}"
  fi
}

trap cleanup EXIT INT TERM

if [[ "${AUTO_BUILD_INDEX}" == "true" && ! -f "${RAG_INDEX_PATH}" ]]; then
  echo "RAG index missing. Building it first ..."
  python3 "${ROOT_DIR}/scripts/build-rag-index.py"
fi

if [[ -f "${PID_FILE}" ]]; then
  existing_pid="$(cat "${PID_FILE}")"
  if kill -0 "${existing_pid}" >/dev/null 2>&1; then
    echo "RAG service already running with PID ${existing_pid}"
  else
    rm -f "${PID_FILE}"
  fi
fi

if [[ ! -f "${PID_FILE}" ]]; then
  echo "Starting RAG service in the background ..."
  nohup "${ROOT_DIR}/scripts/start-rag-service.sh" >>"${LOG_FILE}" 2>&1 &
  rag_pid=$!
  echo "${rag_pid}" >"${PID_FILE}"
  STARTED_RAG="true"
  echo "RAG service PID: ${rag_pid}"
  echo "RAG service log: ${LOG_FILE}"
fi

echo "Starting router service in the foreground ..."
exec "${ROOT_DIR}/scripts/start-router-service.sh"
