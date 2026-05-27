# Local-LLM Architecture

## End-to-End Request Flows
- Open WebUI or API client -> router endpoint -> route heuristic -> selected local model or RAG path -> OpenAI-compatible response

## Frontend / Backend Interaction
- API boundaries are repo-local; inspect the listed entrypoints before changing wire contracts

## Service Boundaries
- Open WebUI + Ollama node
- OpenAI-compatible router service
- optional RAG indexing/runtime path

## Sync vs Async Flows
- routing decisions
- RAG indexing/build jobs
- model inventory/bootstrap scripts

## Event-Driven Architecture
- No dedicated event bus, broker, or queue consumer layer is visible in the inspected files.

## Caching Layers
- Open WebUI connection/model state can stay stale until re-saved or restarted

## Auth Flow
Router-facing auth is intentionally lightweight; Open WebUI connection settings control the main admin surface.

## Deployment Topology
Docker-based local AI node, with single-process router+RAG runtime available through startup scripts.

## Scaling Behavior
- Active repo; scaling pressure will first appear in the data/API boundary rather than in broad service fan-out
- No autoscaling or multi-region story is visible unless infra files explicitly add one

## Resilience Mechanisms
- typed validation and repo-local guardrails where implemented
- manual fallbacks remain part of the operating model for many repos in this workspace

## Failover Behavior
- No formal failover topology is documented; failure handling is mostly local retries, manual restart, or degraded fallback.

## Observability Architecture
- console logs and local UI feedback are the default observability path

## Retry / Idempotency Patterns
- protect state-changing endpoints from duplicate actions where the repo explicitly calls this out
