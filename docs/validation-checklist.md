# Validation Checklist

Run this after local setup or after migration to a new host.

## Base checks

- `./scripts/verify-ollama-models.sh`
- `RUN_SMOKE_TESTS=true ./scripts/verify-ollama-models.sh`
- `./scripts/check-open-webui-connectivity.sh`

## Router mode

- `./scripts/start-router-rag-stack.sh`
- `./scripts/start-router-service.sh`
- `./scripts/check-router-connectivity.sh`
- `RUN_SMOKE_TESTS=true ./scripts/check-router-connectivity.sh`
- in `Admin Settings -> Connections`, enable `http://host.docker.internal:8788/v1` if it exists but is disabled
- confirm `local-ai-node-auto` appears in Open WebUI
- confirm a basic prompt works through `local-ai-node-auto`
- refresh or re-save the OpenAI connection if the router model list looks stale
- confirm direct Ollama mode is disabled when you want router-only behavior
- for grounded answers, confirm the RAG index exists before debugging the UI
- for image prompts, confirm `llava:13b` is installed and the router-backed connection is the one in use

## Scenario checks

- General chat:
  send a normal non-repo prompt and expect route `chat` with model `llama3.1:8b`
- Coding:
  send a coding prompt and expect route `code` with model `deepseek-coder:6.7b`
- Light:
  send a short utility prompt and expect route `light` with model `phi3`
- RAG:
  send a repo/deployment question and expect route `rag` with non-empty `router.sources`
- RAG fallback:
  remove the index temporarily and expect the same repo question to fall back to `chat`
- Vision:
  send an image-bearing request and expect route `vision` with model `llava:13b`
- Context carryover:
  send a short follow-up after coding context and expect it to stay on route `code`
- Manual override:
  send `model: phi3` and expect route `manual`

Use [docs/model-router.md](/Users/basho00/_github/_personal/Local-LLM/docs/model-router.md) for the exact request payloads and expected outputs for each scenario.

## Option A: host Ollama

- `curl http://localhost:11434/api/tags`
- `docker compose up -d`
- open `http://localhost:3000`
- in `Admin Settings -> Connections`, enable `http://host.docker.internal:11434` if it exists but is disabled

## Option B: Docker Ollama

- `docker compose -f docker-compose.yml -f docker-compose.ollama.yml up -d`
- `curl http://localhost:11434/api/tags`
- open `http://localhost:3000`
- in `Admin Settings -> Connections`, enable `http://ollama:11434` if it exists but is disabled

## Operational checks

- confirm the expected models appear in Open WebUI
- confirm a basic chat works with `llama3.1:8b`
- confirm a coding prompt works with `deepseek-coder:6.7b`
- confirm embedding API responses work for `nomic-embed-text`
- if installed, confirm the selected optional large model responds
- if installed, confirm vision prompts work with `llava:13b`
