# Target Host First Pass

Use this sequence for the first deployment on the final Unix/Linux system.

## 1. Clone the repo

```bash
git clone git@github.com:bhavyadalwadi/localLLM.git
cd localLLM
```

## 2. Create the environment file

For a host-based Ollama deployment:

```bash
cp .env.example .env
```

For a quick staging-like setup:

```bash
cp .env.staging.example .env
```

Then edit `.env` for the target host.

## 3. Run preflight

```bash
./scripts/preflight-target-host.sh
```

## 4. Choose the deployment path

Host Ollama:

```bash
docker compose up -d
```

Docker Ollama:

```bash
docker compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
```

## 5. Validate

```bash
./scripts/verify-ollama-models.sh
./scripts/check-open-webui-connectivity.sh
```

## 6. Restore models if needed

```bash
CONFIRM_RESTORE=true ./scripts/restore-ollama-store.sh /path/to/ollama-home-backup
```

If you restore after startup, restart the affected service before validating again.

