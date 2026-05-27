# Local-LLM Project Context

Generated: 2026-05-27 01:50 UTC

## Business Purpose
Local AI Node is a production-friendly self-hosted LLM stack centered on Open WebUI, Ollama, model routing, and future RAG and backup workflows.

## System Overview
This repo centers on Open WebUI + Ollama node, OpenAI-compatible router service, optional RAG indexing/runtime path.

## Major Applications
- Open WebUI + Ollama node
- OpenAI-compatible router service
- optional RAG indexing/runtime path

## Environments
- local development
- containerized local runtime
- production-like deployment only when explicitly documented in README/infra files

## Tech Stack
- Docker
- Shell
- Ollama
- Open WebUI
- Docker Compose

## Critical Dependencies
- No package-manager dependencies were parsed.

## Major Workflows
- Docker-based Open WebUI deployment with Ollama on the host, in Docker, or on a remote node
- Defined core model roles for chat, coding, embeddings, optional larger models, and optional vision
- Bootstrap, preflight, and verification scripts for target-host deployment and model inventory checks
- Planned model-router and RAG scaffolding with dedicated docs and runtime folders
- Backup and restore workflow for the Ollama model store and local AI node data

## Operational Constraints
- Open WebUI can look healthy while the router-backed connection is disabled
- mixed direct-Ollama and router mode can confuse model selection and debugging
- router behavior depends on local model availability and shared RAG index presence

## Scaling Constraints
- This repo has active product or operational intent; changes should assume future iteration rather than a one-off snapshot.

## Deployment Model
Docker-based local AI node, with single-process router+RAG runtime available through startup scripts.

## Important APIs
- `POST /chat`
- `GET /v1/models`
- `POST /v1/chat/completions`

## Important Databases
- No dedicated database is visible from the inspected files.

## Important Queues / Events
- routing decisions
- RAG indexing/build jobs
- model inventory/bootstrap scripts

## Known Technical Debt
- improve routing signals with conversation history and confidence thresholds
- add image-routing support for `llava:13b`
- add incremental index rebuilds instead of full rebuilds
- expose router + RAG service behind one packaged process
- document any remaining UI-side quirks such as model caching or connection

## Current Architecture Themes
- Tier A repo under the `_personal` workspace
- Graphify-first repository discovery
- preserve current architecture instead of speculative rewrites
