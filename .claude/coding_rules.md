# Local-LLM Coding Rules

## Naming / Structure
- Use repo-local naming patterns from the existing modules and manifests
- Keep top-level boundaries stable: `scripts`, `docs`, `configs`, `rag-data`, `backups`, `graphify-out`

## Architecture Patterns
- Read Graphify semantic artifacts before broad source searching when `graphify-out/` exists.
- Preserve existing architecture and make the smallest safe change.

## State Management
- Not present.

## Error Handling / Logging
- Prefer explicit local validation and user-visible failure messages
- Console logging and focused route-level guardrails are the common default
- No centralized observability SDK is visible unless the repo docs say otherwise

## API Conventions
- Preserve current request and response shapes on existing routes
- Do not widen state-changing payloads when the repo is moving toward stronger authority or validation

## Testing Conventions
- No standardized automated test command is visible.

## Typing / Abstractions
- Follow existing typed request/data models where present
- Prefer thin adapters over broad rewrites when integrating providers or services

## Database / Migration Patterns
- Keep schema changes aligned with the repo's chosen persistence layer
- Call out migration or seed prerequisites explicitly when touching stateful flows
- No migration framework is present
