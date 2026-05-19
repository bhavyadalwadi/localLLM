# Repo Semantic Summary - Local-LLM

Generated: 2026-05-19 21:48 UTC

## What This Repo Is For
Local AI Node is a production-friendly self-hosted LLM stack centered on Open WebUI, Ollama, model routing, and future RAG and backup workflows.

## Snapshot
- Domains: ai, devops, tooling
- Tech stack: Docker, Shell, Ollama, Open WebUI
- Pending state: documented
- Status confidence: high
- Current work guess: The active direction is a more capable local router with better signal handling, image routing, and a cleaner packaged runtime.
- Graph stats: 278 nodes · 361 edges · 35 communities (28 shown, 7 thin omitted)

## Features
- Docker-based Open WebUI deployment with Ollama on the host, in Docker, or on a remote node
- Defined core model roles for chat, coding, embeddings, optional larger models, and optional vision
- Bootstrap, preflight, and verification scripts for target-host deployment and model inventory checks
- Planned model-router and RAG scaffolding with dedicated docs and runtime folders
- Backup and restore workflow for the Ollama model store and local AI node data

## Pending
- improve routing signals with conversation history and confidence thresholds
- add image-routing support for `llava:13b`
- add incremental index rebuilds instead of full rebuilds
- expose router + RAG service behind one packaged process
- document any remaining UI-side quirks such as model caching or connection

## Read First
- `README.md`
- `docs/target-host-first-pass.md`
- `docs/model-router.md`
- `docker-compose.yml`

## Likely Entrypoints
- `README.md`
- `docker-compose.yml`
- `docs/model-router.md`
- `scripts/bootstrap-local-ai-node.sh`

## Main Modules
- `scripts`
- `docs`
- `configs`
- `rag-data`
- `backups`

## Conservative Suggestions
- Improve router confidence and conversation-history handling
- Add image-routing support and validate the optional vision path
- Package router and RAG behavior behind a cleaner single-process operator flow

## Evidence Files
- `README.md`
- `docs/model-router.md`
- `docs/target-host-first-pass.md`

## Graph Signals
- God nodes: Local AI Node, Target Host First Pass, generate_text(), build_items(), build_items()
