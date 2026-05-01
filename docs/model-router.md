# Model Router

This repo does not implement an automated router yet, but these are the
intended routing defaults for Open WebUI and any later agent layer.

## Default assignments

- normal chat: `llama3.1:8b`
- coding: `deepseek-coder:6.7b`
- fast/light tasks: `phi3`
- embeddings: `nomic-embed-text`
- optional larger text model: `gemma4:31b` or `qwen3:30b`
- optional vision: `llava:13b`

## Operating rules

- Keep routing explicit and easy to override.
- Do not make the larger model the universal default.
- Use one heavyweight text model at a time in steady-state operation.
- Keep embeddings separate from chat defaults.
- Route image tasks to `llava:13b` only when the prompt actually includes image
  understanding.

## Recommended first-pass UI defaults

- primary default model: `llama3.1:8b`
- coding favorite: `deepseek-coder:6.7b`
- lightweight fallback: `phi3`
- premium text favorite: `gemma4:31b`
- embeddings backend: `nomic-embed-text`

## Later router target

If you add a small routing service later, keep the first version simple:
- text chat -> `llama3.1:8b`
- code tasks -> `deepseek-coder:6.7b`
- low-priority utility prompts -> `phi3`
- complex reasoning by explicit selection -> `gemma4:31b`
- image prompts -> `llava:13b`
