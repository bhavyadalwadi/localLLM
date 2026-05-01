# Local AI Node

This repository is a simple, production-friendly starting point for a target Unix/Linux Local AI Node. It prepares Open WebUI, supports Ollama either on the host or in Docker, and reserves structure for backups, RAG, routing, and later hardening work.

The repo is intended to be the canonical deployment codebase. Push this to Git, migrate it to the final host by cloning, and move model data separately through backup/restore or fresh pulls.

## Planned model roles

- normal chat: `llama3.1:8b`
- coding: `deepseek-coder:6.7b`
- fast/light tasks: `phi3`
- embeddings: `nomic-embed-text`
- optional larger text model: `gemma4:31b` or `qwen3:30b`
- optional vision: `llava:13b`

This repo now treats the four-model core set as the required baseline. Larger
text models and vision are optional so the node stays responsive while Docker,
storage, monitoring, and later RAG services share the machine.

## Repository layout

```text
.
├── .env.example
├── .env.staging.example
├── README.md
├── backups/
├── configs/
│   ├── ollama/
│   └── open-webui/
├── docker-compose.yml
├── docker-compose.ollama.yml
├── docs/
│   ├── model-router.md
│   ├── migration-checklist.md
│   ├── performance-tuning.md
│   ├── rag-pipeline.md
│   ├── security-review.md
│   └── validation-checklist.md
├── rag-data/
│   ├── chroma/
│   ├── documents/
│   └── faiss/
├── scripts/
│   ├── backup-ollama-store.sh
│   ├── check-open-webui-connectivity.sh
│   ├── load-env.sh
│   ├── preflight-target-host.sh
│   ├── restore-ollama-store.sh
│   └── verify-ollama-models.sh
└── volumes/
    ├── ollama-data/
    └── open-webui-data/
```

## Prerequisites

- Docker Engine with Docker Compose plugin
- `curl`
- `rsync`
- Ollama installed on the target host if you use Option A

## Quick start paths

- Current staging machine: `cp .env.staging.example .env`
- Final target host: `cp .env.example .env`
- First target-host deployment guide: [docs/target-host-first-pass.md](/Users/basho00/_github/_personal/Local-LLM/docs/target-host-first-pass.md)

## Step 1: prepare the environment

Copy the example environment file:

```bash
cp .env.example .env
```

If you are using the current staging/download machine, you can start from:

```bash
cp .env.staging.example .env
```

Edit `.env` and choose one `OLLAMA_BASE_URL`:

- Option A, Ollama on the host: `http://host.docker.internal:11434`
- Option B, Ollama in Docker Compose: `http://ollama:11434`

Set a real `WEBUI_SECRET_KEY` before using this beyond a trusted local network.

## Step 2: choose your Ollama deployment mode

### Option A: Ollama on the host

Use this when you want the model store and Ollama runtime managed directly on the Unix/Linux host. This is the default path in this repo.

1. Install Ollama on the host.
2. Restore or copy your staged model store into `~/.ollama` on the target machine.
3. Confirm Ollama is reachable:

```bash
curl http://localhost:11434/api/tags
```

4. Start Open WebUI only:

```bash
docker compose up -d
```

### Option B: Ollama in Docker

Use this when you want both services managed by Docker Compose.

1. Set `OLLAMA_BASE_URL=http://ollama:11434` in `.env`.
2. Start Open WebUI and Ollama together:

```bash
docker compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
```

3. Confirm Ollama is reachable:

```bash
curl http://localhost:11434/api/tags
```

### Option C: Remote Open WebUI host

Use this when Ollama runs on one machine and Open WebUI runs on a different Docker-capable host.

Typical layout:
- this Mac or another node runs Ollama on `11434`
- a separate Linux or Docker host runs Open WebUI
- Open WebUI points to the Ollama node over the network

Example on the Open WebUI host:

```bash
cp .env.example .env
```

Set:

```bash
OLLAMA_BASE_URL=http://OLLAMA_NODE_IP:11434
```

Then start Open WebUI on the remote host:

```bash
docker compose up -d
```

Before doing this, confirm from the Open WebUI host that it can reach the Ollama node:

```bash
curl http://OLLAMA_NODE_IP:11434/api/tags
```

If security policy allows only private network access, keep this traffic on a trusted LAN or VPN.

## Step 3: verify the model inventory

Run the inventory check:

```bash
./scripts/verify-ollama-models.sh
```

Run the full first-pass bootstrap in the expected order:

```bash
./scripts/bootstrap-local-ai-node.sh
```

Include optional models in the validation flow:

```bash
EXPECT_OPTIONAL_MODELS="gemma4:31b,llava:13b" ./scripts/bootstrap-local-ai-node.sh
```

Run target-host preflight before the first deployment:

```bash
./scripts/preflight-target-host.sh
```

Optional smoke tests:

```bash
RUN_SMOKE_TESTS=true ./scripts/verify-ollama-models.sh
RUN_SMOKE_TESTS=true EXPECT_OPTIONAL_MODELS="gemma4:31b,llava:13b" ./scripts/bootstrap-local-ai-node.sh
```

## Download models on a new system

After `ollama` is installed, pull the required core model set with:

```bash
./scripts/pull-required-models.sh
```

Pull a specific optional model with:

```bash
OPTIONAL_MODELS="gemma4:31b" ./scripts/pull-required-models.sh
```

Other valid optional pulls:

```bash
OPTIONAL_MODELS="qwen3:30b" ./scripts/pull-required-models.sh
OPTIONAL_MODELS="llava:13b" ./scripts/pull-required-models.sh
```

Avoid pulling multiple heavyweight text models unless you have a specific need
to compare them. The intended default is one fast general model, one coding
model, one lightweight fallback, one embedding model, and optionally one larger
text model plus vision.

To inspect the exact manifest and blob files for a model before moving it to a
new system, run:

```bash
./scripts/show-model-files.sh gemma4:31b
./scripts/show-model-files.sh llava:13b
```

This prints the manifest path plus every blob file referenced by that model.

## First RAG workflow

The repo now includes a minimal local RAG path built on top of Ollama
embeddings, a local JSON index, and a small local HTTP service.

1. Put source files in `rag-data/documents/`.
2. Build the index:

```bash
python3 ./scripts/build-rag-index.py
```

3. Inspect retrieval results:

```bash
python3 ./scripts/query-rag.py "What models are part of the core stack?"
```

4. Generate an answer from retrieved context:

```bash
python3 ./scripts/rag-answer.py "What is the deployment flow for the target host?"
```

Use `RAG_CHAT_MODEL=gemma4:31b` when you want a stronger final answer model.

## How This Actually Works

`rag-data/documents/` is the source-of-truth context directory for the first
RAG implementation. Put the text material you want the system to know there:
- notes
- docs
- runbooks
- config references
- logs you want to search

The current pipeline is:
1. `build-rag-index.py` reads files from `rag-data/documents/`
2. it chunks the text
3. it embeds each chunk with `nomic-embed-text`
4. it writes a local index to `rag-data/chroma/rag-index.json`
5. `query-rag.py` and `rag-answer.py` retrieve relevant chunks
6. the final answer is generated with `llama3.1:8b` or `gemma4:31b`

## Open WebUI Relationship

Open WebUI still works, but not automatically with this custom RAG path.

What Open WebUI does right now:
- lets you chat with Ollama models manually
- lets you choose `llama3.1:8b`, `gemma4:31b`, `llava:13b`, and others

What Open WebUI does not do yet in this repo:
- call `build-rag-index.py`
- call `query-rag.py`
- call `rag-answer.py`
- automatically use `rag-data/documents/` as grounded context

That means the stronger system is now split into two layers:
- Open WebUI for direct model access
- local RAG scripts and service for grounded answers

The bridge layer is the new local RAG service:

```bash
./scripts/start-rag-service.sh
```

It exposes local endpoints for health, index build, retrieval, and grounded
answer generation. That service is what we can wire into future agent or UI
integration.

Example:

```bash
curl -X POST http://127.0.0.1:8787/answer \
  -H "Content-Type: application/json" \
  -d '{"query":"What is our deployment flow?","model":"gemma4:31b"}'
```

## Smart Router API

The repo now also includes a single smart router endpoint so callers do not
need to choose a model manually every time.

Start it:

```bash
./scripts/start-router-service.sh
```

Health check:

```bash
curl http://127.0.0.1:8788/health
```

Simple chat endpoint:

```bash
curl -X POST http://127.0.0.1:8788/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What is our target architecture?"}'
```

OpenAI-style endpoint:

```bash
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"local-ai-node-auto",
    "messages":[
      {"role":"user","content":"What is our deployment flow?"}
    ],
    "stream":false
  }'
```

Router behavior today:
- repo and node questions use the RAG path
- coding questions use `deepseek-coder:6.7b`
- short utility prompts can use `phi3`
- general chat falls back to `llama3.1:8b`

This is the path to the UI talking to one endpoint directly instead of asking
you to choose a model every time.

## Open WebUI Through The Router

The recommended end-state is:
- Open WebUI talks to the router, not directly to Ollama
- the router decides whether to use RAG, coding, light, or normal chat
- Open WebUI uses the router's OpenAI-compatible endpoint
- the default model in the UI becomes `local-ai-node-auto`

Repo defaults now support that mode through environment variables in
`.env.example` and `.env.staging.example`.

### Recommended startup order

1. Make sure Ollama is running on the host.
2. Build the RAG index:

```bash
python3 ./scripts/build-rag-index.py
```

3. Start the router:

```bash
./scripts/start-router-service.sh
```

4. Start Open WebUI:

```bash
docker compose up -d
```

### Router-mode Open WebUI settings

Recommended `.env` values:

```bash
ENABLE_OLLAMA_API=false
ENABLE_OPENAI_API=true
OPENAI_API_BASE_URL=http://host.docker.internal:8788/v1
OPENAI_API_KEY=local-ai-node
```

### What you should see in the UI

- an OpenAI-compatible backend provided by the local router
- the `local-ai-node-auto` model id available from the model list
- one default model choice in the UI that routes automatically underneath

This does not eliminate the model selector from Open WebUI itself, but it means
you can keep the UI on `local-ai-node-auto` for normal use instead of manually
switching between `llama3.1`, `deepseek-coder`, `phi3`, and `gemma4`.

## Step 4: verify Open WebUI connectivity

Run the connectivity check:

```bash
./scripts/check-open-webui-connectivity.sh
```

Then open:

```text
http://localhost:3000
```

## No-Docker note

If Docker is unavailable, the host-based Ollama path still works.

What still works without Docker:
- Ollama model serving
- model verification
- generation and embedding smoke tests
- backup and restore
- repo development and migration prep

What does not work from this repo without Docker:
- the packaged Open WebUI Compose deployment
- the Dockerized Ollama option

If Docker is blocked but Python or Node package installs are allowed, a non-Docker Open WebUI install may still be possible in user space. This machine has Python, pip, Node, and npm available, so that path is worth checking if you want UI access before the final Linux deployment.

## Step 5: back up or restore the Ollama model store

Back up `~/.ollama` to the backup path in `.env`:

```bash
./scripts/backup-ollama-store.sh
```

Restore from a specific backup:

```bash
CONFIRM_RESTORE=true ./scripts/restore-ollama-store.sh /mnt/nas/local-ai-node/ollama-backups/ollama-home-YYYYMMDD-HHMMSS
```

The restore script creates a safety backup of the current target directory before copying data in.

### Backup path examples

Local directory:

```bash
BACKUP_ROOT_DIR=$HOME/local-ai-node/backups
```

Mounted NAS on macOS:

```bash
BACKUP_ROOT_DIR=/Volumes/MyNAS/local-ai-node-backups
```

Mounted NAS on Linux:

```bash
BACKUP_ROOT_DIR=/mnt/nas/local-ai-node-backups
```

To confirm what your current `.env` is set to:

```bash
grep -E '^(BACKUP_ROOT_DIR|OLLAMA_HOME_DIR)=' .env
```

## Notes on migration

- Keep this repo in Git and treat it as the deployment source of truth.
- Move model data separately from Git.
- Host-based Ollama is the simpler path if you want direct control over `~/.ollama`.
- Docker-based Ollama is easier to keep self-contained but may complicate migrations if you later switch storage layouts.
- A NAS can be used for backup and migration, but it is not required and should not be the live Ollama model directory.

Use [docs/migration-checklist.md](/Users/basho00/_github/_personal/Local-LLM/docs/migration-checklist.md) before moving to another host and [docs/validation-checklist.md](/Users/basho00/_github/_personal/Local-LLM/docs/validation-checklist.md) after setup.

For host-based Ollama service management, see [configs/ollama/systemd-setup.md](/Users/basho00/_github/_personal/Local-LLM/configs/ollama/systemd-setup.md) and [configs/ollama/ollama.service](/Users/basho00/_github/_personal/Local-LLM/configs/ollama/ollama.service).

## Future work

Operational guidance is included in [docs/rag-pipeline.md](/Users/basho00/_github/_personal/Local-LLM/docs/rag-pipeline.md), [docs/model-router.md](/Users/basho00/_github/_personal/Local-LLM/docs/model-router.md), [docs/security-review.md](/Users/basho00/_github/_personal/Local-LLM/docs/security-review.md), and [docs/performance-tuning.md](/Users/basho00/_github/_personal/Local-LLM/docs/performance-tuning.md).

RAG is intentionally not implemented here. When you add it, start with `nomic-embed-text` plus either Chroma or FAISS and keep ingestion/persistence separate from the base Ollama/Open WebUI stack.
