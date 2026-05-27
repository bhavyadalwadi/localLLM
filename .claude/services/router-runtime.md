# Router Runtime

## Responsibility
Expose one OpenAI-compatible entrypoint that chooses routing strategy and model.

## Dependencies
- Docker
- Shell
- Ollama
- Open WebUI
- Docker Compose

## Inbound APIs
- `POST /chat`
- `GET /v1/models`
- `POST /v1/chat/completions`

## Outbound APIs
- `POST /chat`
- `GET /v1/models`
- `POST /v1/chat/completions`

## Databases Used
- No database visible.

## Queues / Topics
- routing decisions
- RAG indexing/build jobs
- model inventory/bootstrap scripts

## Critical Workflows
- route selection
- RAG grounding
- OpenAI-compatible compatibility surface

## Failure Modes
- Open WebUI can look healthy while the router-backed connection is disabled
- mixed direct-Ollama and router mode can confuse model selection and debugging
- router behavior depends on local model availability and shared RAG index presence

## Scaling Concerns
- scale pressure will show up first in the stateful/data boundary
- no heavyweight horizontal scaling layer is visible from the repo docs

## Operational Concerns
- validate environment and schema prerequisites before changing behavior
- use the repo-local docs in `.claude/` plus Graphify entrypoints before editing

## Important Source Files
- `README.md`
- `docker-compose.yml`
- `docs/model-router.md`
- `scripts/bootstrap-local-ai-node.sh`
- `README.MD`
- `docs/target-host-first-pass.md`

## Dangerous Code Paths
- Open WebUI can look healthy while the router-backed connection is disabled
- mixed direct-Ollama and router mode can confuse model selection and debugging
- router behavior depends on local model availability and shared RAG index presence

## Testing Strategy
- No standardized automated test command is visible.

## Known Technical Debt
- improve routing signals with conversation history and confidence thresholds
- add image-routing support for `llava:13b`
- add incremental index rebuilds instead of full rebuilds
- expose router + RAG service behind one packaged process
- document any remaining UI-side quirks such as model caching or connection
