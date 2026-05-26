# Model Router

This repo now includes a first-pass local router service. It provides one smart
entrypoint that can choose a route and model for the request instead of forcing
manual model selection every time.

## Current plan

- Keep the base repo centered on a reliable Ollama + Open WebUI node.
- Keep router and RAG as add-on behavior, not a broader platform.
- Keep the router as the OpenAI-compatible front door.
- Keep the runtime operationally simple enough to validate on another machine.

## Current status

- The base node plan is unchanged.
- Router heuristics are implemented.
- RAG index build, query, and grounded-answer flow are implemented.
- The packaged router + RAG path now has a single-process runtime:
  - `scripts/local_ai_runtime.py`
  - `scripts/start-local-ai-runtime.sh`
- `scripts/start-router-rag-stack.sh` remains as a thin compatibility launcher.
- The next step is validation on another system, not more feature expansion.

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
- `scripts/local_ai_runtime.py`
- `scripts/start-local-ai-runtime.sh`
- `scripts/start-router-service.sh`
- `scripts/start-router-rag-stack.sh`
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
- or start the single-process runtime with `./scripts/start-local-ai-runtime.sh`
- `./scripts/start-router-rag-stack.sh` is still valid as a compatibility wrapper
- validate it with `./scripts/check-router-connectivity.sh`
- run `RUN_SMOKE_TESTS=true ./scripts/check-router-connectivity.sh` for a live completion check
- in Open WebUI admin settings, enable the OpenAI connection for `http://host.docker.internal:8788/v1` if it exists but is disabled

## Current routing behavior

- local repo, deployment, architecture, security, migration, and RAG questions
  go through the RAG path and default to `gemma4:31b`
- coding questions go to `deepseek-coder:6.7b`
- messages with image input route to `llava:13b`
- short utility prompts can go to `phi3`
- everything else falls back to `llama3.1:8b`
- recent conversation context now contributes to routing instead of only the
  last user turn
- weak single-keyword matches fall back to normal chat unless they cross a
  small confidence threshold

If a caller explicitly requests a real model id, the router honors that instead
of auto-routing.

## Recommended first-pass UI defaults

- primary default model: `llama3.1:8b`
- coding favorite: `deepseek-coder:6.7b`
- lightweight fallback: `phi3`
- premium text favorite: `gemma4:31b`
- embeddings backend: `nomic-embed-text`

## Open WebUI behavior notes

- If Open WebUI loads but `local-ai-node-auto` is missing, check `Admin Settings -> Connections` first and re-enable `http://host.docker.internal:8788/v1` if it exists but is disabled.
- Open WebUI may keep older connection state or model-list state until the connection is re-saved or the page is refreshed.
- Keep router mode simple: use the router-backed OpenAI connection as the main path and disable direct Ollama mode in `.env` when you want predictable behavior.
- The model selector still appears in Open WebUI. Router mode does not remove that UI; it makes `local-ai-node-auto` the normal default choice.
- If the UI shows both direct Ollama models and router-backed models, verify whether `ENABLE_OLLAMA_API` is still on. Mixed mode can be useful for debugging but is noisier for normal operation.
- If RAG-backed answers seem missing, check the router health endpoint and confirm the shared RAG index file exists before assuming the UI is the issue.
- If image prompts do not behave as expected, verify that the request is actually going through the router-backed connection and that `llava:13b` is installed on the Ollama host.
- After changing router-mode environment values, restart Open WebUI and re-check the saved connection state in the admin UI.

## Router-mode troubleshooting

- Symptom: Open WebUI loads but no router model appears.
  Check the OpenAI connection entry in `Admin Settings -> Connections`, then run `./scripts/check-router-connectivity.sh`.
- Symptom: `local-ai-node-auto` appears but responses look like plain chat.
  Confirm the prompt is being sent through the router-backed connection and that the RAG index exists at the expected path.
- Symptom: repo questions do not use grounded answers.
  Rebuild the index with `python3 ./scripts/build-rag-index.py`, then re-run the router connectivity check.
- Symptom: image prompts fail or ignore the image.
  Confirm `llava:13b` is installed, the payload includes image input, and the active connection is the router endpoint rather than direct Ollama.
- Symptom: the UI still shows stale models after config changes.
  Re-save the connection, refresh the page, and if needed restart Open WebUI so the new backend state is picked up cleanly.

## Step-by-step validation scenarios

Use the router health check first:

```bash
./scripts/check-router-connectivity.sh
```

For API-level validation, prefer the OpenAI-style endpoint because it exposes
router metadata in the response body.

### Scenario 1: General chat fallback

Input:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"local-ai-node-auto",
    "messages":[
      {"role":"user","content":"Give me a two sentence pep talk for the afternoon."}
    ],
    "stream":false
  }'
```

Expected route:
- route: `chat`
- selected model: `llama3.1:8b`

Expected output shape:
- response includes `router.route` = `chat`
- response includes `router.selected_model` = `llama3.1:8b`
- answer is a normal direct response and `router.sources` is empty

### Scenario 2: Coding route

Input:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"local-ai-node-auto",
    "messages":[
      {"role":"user","content":"Write a Python function to deduplicate a list while preserving order."}
    ],
    "stream":false
  }'
```

Expected route:
- route: `code`
- selected model: `deepseek-coder:6.7b`

Expected output shape:
- response includes `router.route` = `code`
- response includes `router.selected_model` = `deepseek-coder:6.7b`
- answer should look like a coding answer, not grounded repo retrieval

### Scenario 3: Light/short route

Input:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"local-ai-node-auto",
    "messages":[
      {"role":"user","content":"one line: what is docker?"}
    ],
    "stream":false
  }'
```

Expected route:
- route: `light`
- selected model: `phi3`

Expected output shape:
- response includes `router.route` = `light`
- response includes `router.selected_model` = `phi3`
- answer is short and direct

### Scenario 4: RAG route for repo knowledge

Precondition:
- the RAG index exists at `rag-data/chroma/rag-index.json`

Input:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"local-ai-node-auto",
    "messages":[
      {"role":"user","content":"What is our target-host deployment flow for this repo?"}
    ],
    "stream":false
  }'
```

Expected route:
- route: `rag`
- selected model: `gemma4:31b` unless overridden by env

Expected output shape:
- response includes `router.route` = `rag`
- response includes non-empty `router.sources`
- answer should mention repo-grounded deployment steps rather than generic deployment advice

### Scenario 5: RAG fallback when index is missing

Precondition:
- temporarily move or remove the active RAG index file

Input:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"local-ai-node-auto",
    "messages":[
      {"role":"user","content":"What does this repo say about backup and restore?"}
    ],
    "stream":false
  }'
```

Expected route:
- route falls back to `chat`
- selected model falls back to `llama3.1:8b`

Expected output shape:
- response includes `router.reason` mentioning missing RAG index fallback
- `router.sources` is empty

### Scenario 6: Vision route with image input

Precondition:
- `llava:13b` is installed on the Ollama host

Input shape:

```json
{
  "model": "local-ai-node-auto",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What is in this image?"},
        {"type": "image_url", "image_url": {"url": "file:///absolute/path/to/test-image.jpg"}}
      ]
    }
  ],
  "stream": false
}
```

Expected route:
- route: `vision`
- selected model: `llava:13b`

Expected output shape:
- response includes `router.route` = `vision`
- response includes `router.selected_model` = `llava:13b`
- answer describes the image content instead of ignoring it

### Scenario 7: Recent conversation influences routing

Input:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"local-ai-node-auto",
    "messages":[
      {"role":"user","content":"I am debugging a Python API handler."},
      {"role":"assistant","content":"What part is failing?"},
      {"role":"user","content":"Now help me fix this function."}
    ],
    "stream":false
  }'
```

Expected route:
- route: `code`
- selected model: `deepseek-coder:6.7b`

Expected output shape:
- router should still choose `code` even though the final message alone is less explicit
- this confirms recent conversation context is being used

### Scenario 8: Weak keyword should not force RAG

Input:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"local-ai-node-auto",
    "messages":[
      {"role":"user","content":"Give me a fun story about security guards on Mars."}
    ],
    "stream":false
  }'
```

Expected route:
- route: `chat`

Expected output shape:
- the single keyword `security` should not by itself force RAG
- `router.sources` should be empty

### Scenario 9: Manual model override

Input:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"phi3",
    "messages":[
      {"role":"user","content":"What is our deployment flow?"}
    ],
    "stream":false
  }'
```

Expected route:
- route: `manual`
- selected model: `phi3`

Expected output shape:
- response includes `router.reason` = `explicit model override`
- router should honor the requested model instead of auto-routing to RAG

## Detailed test plan

1. Start the stack.
   - Run `./scripts/start-local-ai-runtime.sh`
   - Or run `./scripts/start-router-rag-stack.sh` if you want the old entrypoint name
   - Run `./scripts/check-router-connectivity.sh`

2. Validate base router health.
   - Confirm `/health` responds.
   - Confirm `/v1/models` includes `local-ai-node-auto`.

3. Validate non-grounded routes.
   - Run Scenario 1 for chat fallback.
   - Run Scenario 2 for coding.
   - Run Scenario 3 for light routing.

4. Validate grounded routing.
   - Build the index with `python3 ./scripts/build-rag-index.py`.
   - Run Scenario 4 and confirm `router.sources` is populated.
   - Run Scenario 5 only if you want to prove fallback behavior when the index is absent.

5. Validate multimodal routing.
   - Confirm `llava:13b` is installed.
   - Run Scenario 6 and confirm the route is `vision`.

6. Validate routing heuristics.
   - Run Scenario 7 to prove recent conversation context affects the route.
   - Run Scenario 8 to prove weak keywords do not force RAG.

7. Validate override behavior.
   - Run Scenario 9 and confirm explicit model selection bypasses auto-routing.

8. Validate UI behavior through Open WebUI.
   - Select `local-ai-node-auto`.
   - Repeat one repo-grounded question and one normal chat prompt.
   - Confirm grounded prompts behave like Scenario 4 and normal chat behaves like Scenario 1.
   - If results differ from API tests, inspect the saved Open WebUI connection rather than assuming router logic is wrong.

## Status

- [x] router signal improvements via recent conversation context and a simple
  confidence threshold
- [x] `llava:13b` image routing
- [x] incremental index rebuilds
- [x] packaged router + RAG operator flow
- [x] single-process packaged runtime
- [x] heavier router/Open WebUI behavior docs
