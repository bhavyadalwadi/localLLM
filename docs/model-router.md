# Model Router

This repo now includes a first-pass local router service. It provides one smart
entrypoint that can choose a route and model for the request instead of forcing
manual model selection every time.

## Default assignments

- normal chat: `llama3.1:8b`
- coding: `deepseek-coder:6.7b`
- fast/light tasks: `phi3`
- embeddings: `nomic-embed-text`
- optional larger text model: `gemma4:31b` or `qwen3:30b`
- optional vision: `llava:13b`

## Operating rules

- Keep routing explicit and easy to override.
- Do not make the larger model the universal default.
- Use one heavyweight text model at a time in steady-state operation.
- Keep embeddings separate from chat defaults.
- Route image tasks to `llava:13b` only when the prompt actually includes image
  understanding.

## Current router service

Scripts:
- `scripts/router_service.py`
- `scripts/start-router-service.sh`
- `scripts/check-router-connectivity.sh`

Endpoints:
- `POST /chat`
- `GET /v1/models`
- `POST /v1/chat/completions`

OpenAI-style model id:
- `local-ai-node-auto`

## UI integration target

Recommended UI architecture:
- Open WebUI connects to the router's OpenAI-compatible endpoint
- Open WebUI default selected model is `local-ai-node-auto`
- the router decides when to use RAG, coding, light, or normal chat

Recommended environment values for Open WebUI:
- `ENABLE_OLLAMA_API=false`
- `ENABLE_OPENAI_API=true`
- `OPENAI_API_BASE_URL=http://host.docker.internal:8788/v1`
- `OPENAI_API_KEY=local-ai-node`

Recommended startup validation:
- start the router with `./scripts/start-router-service.sh`
- validate it with `./scripts/check-router-connectivity.sh`
- run `RUN_SMOKE_TESTS=true ./scripts/check-router-connectivity.sh` for a live completion check
- in Open WebUI admin settings, enable the OpenAI connection for `http://host.docker.internal:8788/v1` if it exists but is disabled

## Current routing behavior

- local repo, deployment, architecture, security, migration, and RAG questions
  go through the RAG path and default to `gemma4:31b`
- coding questions go to `deepseek-coder:6.7b`
- short utility prompts can go to `phi3`
- everything else falls back to `llama3.1:8b`

If a caller explicitly requests a real model id, the router honors that instead
of auto-routing.

## Recommended first-pass UI defaults

- primary default model: `llama3.1:8b`
- coding favorite: `deepseek-coder:6.7b`
- lightweight fallback: `phi3`
- premium text favorite: `gemma4:31b`
- embeddings backend: `nomic-embed-text`

## TODO

- improve routing signals with conversation history and confidence thresholds
- add image-routing support for `llava:13b`
- add incremental index rebuilds instead of full rebuilds
- expose router + RAG service behind one packaged process
- document any remaining UI-side quirks such as model caching or connection
  persistence after router mode is used more heavily
