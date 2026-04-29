# Local AI Node

This repository is a simple, production-friendly starting point for a target Unix/Linux Local AI Node. It prepares Open WebUI, supports Ollama either on the host or in Docker, and reserves structure for backups, RAG, routing, and later hardening work.

The repo is intended to be the canonical deployment codebase. Push this to Git, migrate it to the final host by cloning, and move model data separately through backup/restore or fresh pulls.

## Planned model roles

- normal chat: `llama3:8b`
- coding: `deepseek-coder:6.7b`
- fast/light tasks: `phi3`
- mid-tier reasoning: `mixtral:8x7b`
- heavy reasoning: `llama3:70b`
- vision: `llava:13b`
- embeddings: `nomic-embed-text`
- optional extra: `gemma4:31b`

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

Run target-host preflight before the first deployment:

```bash
./scripts/preflight-target-host.sh
```

Optional smoke tests:

```bash
RUN_SMOKE_TESTS=true ./scripts/verify-ollama-models.sh
```

## Download models on a new system

After `ollama` is installed, pull the required model set with:

```bash
./scripts/pull-required-models.sh
```

Include the optional `gemma4:31b` model with:

```bash
INCLUDE_OPTIONAL=true ./scripts/pull-required-models.sh
```

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

Placeholders are included in [docs/rag-pipeline.md](/Users/basho00/_github/_personal/Local-LLM/docs/rag-pipeline.md), [docs/model-router.md](/Users/basho00/_github/_personal/Local-LLM/docs/model-router.md), [docs/security-review.md](/Users/basho00/_github/_personal/Local-LLM/docs/security-review.md), and [docs/performance-tuning.md](/Users/basho00/_github/_personal/Local-LLM/docs/performance-tuning.md).

RAG is intentionally not implemented here. When you add it, start with `nomic-embed-text` plus either Chroma or FAISS and keep ingestion/persistence separate from the base Ollama/Open WebUI stack.
