# Migration Checklist

Use this repo as the source of truth for deployment logic. Move model data separately.

## Before migration

- push the latest repo changes to Git
- confirm `.env` values for the target host
- verify the Ollama model inventory on the staging machine
- create a backup of the Ollama model store
- record which deployment mode you want on the target host:
  - host Ollama
  - Docker Ollama

## On the target host

- clone the repo
- copy `.env.example` to `.env`
- adjust `OLLAMA_BASE_URL`, ports, secret key, and backup path
- restore the Ollama model store if you are migrating existing models
- start the selected stack
- run the validation checklist

## Migration rule

Keep source-controlled deployment files in Git. Keep model artifacts out of Git.

