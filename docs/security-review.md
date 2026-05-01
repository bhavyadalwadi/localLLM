# Security Review

This stack is intended to start on a trusted local network and only later be
hardened for broader access. Treat that boundary explicitly.

## Minimum baseline

- Keep Ollama bound to the local host or trusted LAN only.
- Set a real `WEBUI_SECRET_KEY` in `.env`.
- Do not expose Open WebUI directly to the public internet.
- Store backups on a separate path from the live model directory.
- Keep the live Ollama store on local disk.

## Access model

Preferred early-stage posture:
- Ollama accessible only on the host
- Open WebUI accessible only on the trusted LAN
- no direct public exposure

If remote access is required, put Open WebUI behind:
- a VPN, or
- a reverse proxy with TLS and authentication

Do not publish the Ollama API directly unless you have a strong reason and
understand the implications.

## Secrets and configuration

Before real use, review:
- `.env`
- `WEBUI_SECRET_KEY`
- `OLLAMA_BASE_URL`
- any reverse-proxy credentials if added later

Do not commit real secrets to Git.

## Backup handling

- Treat `~/.ollama` backups as sensitive operational assets.
- Keep backup destinations access-controlled.
- If backups leave the local disk or trusted LAN, encrypt them.
- Test restore procedures on a non-production path before relying on them.

## Operational review points

- Confirm Docker services are only publishing intended ports.
- Confirm Open WebUI is reachable only where expected.
- Confirm NAS mounts are not used as the live Ollama model directory.
- Confirm copied model stores preserve ownership and permissions.

## Later hardening

When the node is stable, review:
- reverse proxy with TLS
- authenticated remote access
- service supervision and restart policy
- host firewall rules
- backup encryption and rotation
