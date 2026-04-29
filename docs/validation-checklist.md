# Validation Checklist

Run this after local setup or after migration to a new host.

## Base checks

- `./scripts/verify-ollama-models.sh`
- `RUN_SMOKE_TESTS=true ./scripts/verify-ollama-models.sh`
- `./scripts/check-open-webui-connectivity.sh`

## Option A: host Ollama

- `curl http://localhost:11434/api/tags`
- `docker compose up -d`
- open `http://localhost:3000`

## Option B: Docker Ollama

- `docker compose -f docker-compose.yml -f docker-compose.ollama.yml up -d`
- `curl http://localhost:11434/api/tags`
- open `http://localhost:3000`

## Operational checks

- confirm the expected models appear in Open WebUI
- confirm a basic chat works with `llama3:8b`
- confirm a coding prompt works with `deepseek-coder:6.7b`
- confirm embedding API responses work for `nomic-embed-text`

