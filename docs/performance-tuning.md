# Performance Tuning

Use this guide to keep the node responsive while running local models alongside
Docker services, storage mounts, monitoring, and later RAG jobs.

## Core rule

Optimize for stable throughput, not the largest possible model.

For this project, that means:
- keep `llama3.1:8b` as the default chat model
- use `deepseek-coder:6.7b` only when coding quality matters
- use `phi3` when you want the lightest footprint
- run only one heavyweight text model at a time during normal use

## Model roles and expected pressure

Low pressure:
- `phi3`
- `nomic-embed-text`
- `deepseek-coder:6.7b`
- `llama3.1:8b`

Higher pressure:
- `llava:13b`
- `gemma4:31b`

Avoid as steady-state defaults on shared hardware:
- `mixtral:8x7b`
- `llama3:70b`

## Default operating pattern

Recommended steady-state setup:
- Open WebUI up
- Ollama running on the host
- `llama3.1:8b` as the default chat target
- `gemma4:31b` used only when a prompt justifies it
- `llava:13b` used only for image tasks

This keeps memory pressure predictable and reduces model thrash.

## Practical tuning rules

- Do not keep switching between multiple large models during normal sessions.
- Finish a `gemma4:31b` task, then return to `llama3.1:8b`.
- Use `phi3` for utility prompts, summaries, and low-value background work.
- Keep embeddings separate from chat traffic where possible.
- Prefer host-based Ollama over Dockerized Ollama on Apple Silicon unless you
  need container isolation for a specific reason.

## Validation checks

Measure the system under your normal workload:

```bash
ollama list
docker compose ps
```

Then test:
- one chat with `llama3.1:8b`
- one coding prompt with `deepseek-coder:6.7b`
- one larger reasoning prompt with `gemma4:31b`
- one image prompt with `llava:13b`

If Open WebUI becomes sluggish or background services stall, reduce concurrent
use of the larger models before changing the architecture.

## Migration and backup notes

- Keep the live model store on local disk, not on a NAS mount.
- Use a NAS only for backup and restore.
- When moving large models between systems, copy the Ollama store or use the
  manifest/blob helper script to move only the required files.
