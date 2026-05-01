# Target Host First Pass

Use this sequence for the first deployment on the final host. The intended
default is host-based Ollama plus Dockerized Open WebUI.

## Final baseline

Required core models:
- `llama3.1:8b`
- `deepseek-coder:6.7b`
- `phi3`
- `nomic-embed-text`

Optional models on the target host:
- `gemma4:31b`
- `llava:13b`

Current preferred layout:
- Ollama runs directly on the host
- Open WebUI runs in Docker Compose
- model data lives in `~/.ollama`
- backups go to a separate disk or NAS path

## 1. Clone the repo

```bash
git clone git@github.com:bhavyadalwadi/localLLM.git
cd localLLM
```

## 2. Create the environment file

Use the host-based Ollama path unless you have a specific reason to containerize
Ollama too.

```bash
cp .env.example .env
```

Then edit `.env` for the target host.

Required values to review:
- `OLLAMA_BASE_URL=http://host.docker.internal:11434`
- `WEBUI_SECRET_KEY`
- `BACKUP_ROOT_DIR`
- `OPEN_WEBUI_URL`

## 3. Confirm Ollama is installed and healthy on the host

```bash
ollama --version
curl http://localhost:11434/api/tags
```

If models were copied from another system, confirm the expected inventory:

```bash
ollama list
```

## 4. Run repo preflight

```bash
./scripts/preflight-target-host.sh
```

## 5. Validate or restore the model inventory

If the target host already has the intended models:

```bash
./scripts/verify-ollama-models.sh
EXPECT_OPTIONAL_MODELS="gemma4:31b,llava:13b" ./scripts/verify-ollama-models.sh
```

If the host needs fresh pulls:

```bash
./scripts/pull-required-models.sh
OPTIONAL_MODELS="gemma4:31b,llava:13b" ./scripts/pull-required-models.sh
```

If the host needs a copied Ollama store:

```bash
CONFIRM_RESTORE=true ./scripts/restore-ollama-store.sh /path/to/ollama-home-backup
```

If you restore after startup, restart Ollama before validating again.

## 6. Start Open WebUI

```bash
docker compose up -d
```

Use the Dockerized Ollama path only if you intentionally want both services
inside Compose:

```bash
docker compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
```

## 7. Validate the stack

```bash
./scripts/check-open-webui-connectivity.sh
RUN_SMOKE_TESTS=true ./scripts/verify-ollama-models.sh
```

In Open WebUI, confirm:
- general chat works with `llama3.1:8b`
- coding prompts work with `deepseek-coder:6.7b`
- embeddings are available through `nomic-embed-text`
- `gemma4:31b` responds if installed
- `llava:13b` responds to image prompts if installed

## 8. Set the first routing defaults

Recommended defaults:
- default chat: `llama3.1:8b`
- coding workspace: `deepseek-coder:6.7b`
- low-memory fallback: `phi3`
- embeddings: `nomic-embed-text`
- premium text: `gemma4:31b`
- vision: `llava:13b`

Do not make `gemma4:31b` the global default until you confirm the machine stays
responsive under your normal background load.
