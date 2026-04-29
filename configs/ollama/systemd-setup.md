# Ollama systemd setup

Use this only for Option A where Ollama runs on the host.

## Suggested host layout

- service user: `ollama`
- working directory: `/var/lib/ollama`
- model path: `/var/lib/ollama/.ollama/models`
- listen address: `0.0.0.0:11434`

## Example steps

Create the service account:

```bash
sudo useradd --system --create-home --home-dir /var/lib/ollama --shell /usr/sbin/nologin ollama
```

Create the working directories:

```bash
sudo mkdir -p /var/lib/ollama/.ollama/models
sudo chown -R ollama:ollama /var/lib/ollama
```

Install the service file:

```bash
sudo cp configs/ollama/ollama.service /etc/systemd/system/ollama.service
sudo systemctl daemon-reload
sudo systemctl enable --now ollama
```

Check service health:

```bash
systemctl status ollama --no-pager
curl http://localhost:11434/api/tags
```

## Notes

- If `ollama` is installed in a different path, update `ExecStart`.
- If you want host-only access, set `OLLAMA_HOST=127.0.0.1:11434` and adjust Open WebUI placement accordingly.
- Keep the model directory on local disk, not on a NAS mount.

