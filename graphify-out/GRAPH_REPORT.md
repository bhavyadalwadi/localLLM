# Graph Report - Local-LLM  (2026-05-19)

## Corpus Check
- 35 files · ~9,352 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 278 nodes · 361 edges · 35 communities (28 shown, 7 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 50 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 23|Community 23]]

## God Nodes (most connected - your core abstractions)
1. `Local AI Node` - 19 edges
2. `Target Host First Pass` - 10 edges
3. `generate_text()` - 9 edges
4. `build_items()` - 9 edges
5. `build_items()` - 9 edges
6. `main()` - 8 edges
7. `embed_text()` - 8 edges
8. `build_chat_result()` - 8 edges
9. `RouterHandler` - 8 edges
10. `Model Router` - 8 edges

## Surprising Connections (you probably didn't know these)
- `default_model()` --calls--> `chat_model()`  [INFERRED]
  scripts/router_service.py → scripts/rag_lib.py
- `main()` --calls--> `index_path()`  [INFERRED]
  scripts/router_service.py → scripts/rag_lib.py
- `build_chat_result()` --calls--> `top_k()`  [INFERRED]
  scripts/router_service.py → scripts/rag_lib.py
- `build_direct_response()` --calls--> `generate_text()`  [INFERRED]
  scripts/router_service.py → scripts/rag_lib.py
- `main()` --calls--> `index_path()`  [INFERRED]
  scripts/rag-answer.py → scripts/rag_lib.py

## Communities (35 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (35): build_items(), main(), main(), main(), build_answer_prompt(), build_index_payload(), chat_model(), chunk_overlap() (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (40): code:text (.), code:bash (./scripts/verify-ollama-models.sh), code:bash (./scripts/bootstrap-local-ai-node.sh), code:bash (EXPECT_OPTIONAL_MODELS="gemma4:31b,llava:13b" ./scripts/boot), code:bash (./scripts/preflight-target-host.sh), code:bash (RUN_SMOKE_TESTS=true ./scripts/verify-ollama-models.sh), code:bash (./scripts/pull-required-models.sh), code:bash (OPTIONAL_MODELS="gemma4:31b" ./scripts/pull-required-models.) (+32 more)

### Community 2 - "Community 2"
Cohesion: 0.17
Nodes (15): build_chat_result(), build_direct_response(), classify_route(), code_model(), default_model(), extract_last_user_text(), light_model(), main() (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (21): 1. Clone the repo, 2. Create the environment file, 3. Confirm Ollama is installed and healthy on the host, 4. Run repo preflight, 5. Validate or restore the model inventory, 6. Start Open WebUI, 7. Validate the stack, 8. Set the first routing defaults (+13 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (18): Build the index, code:bash (python3 ./scripts/build-rag-index.py), code:bash (curl -X POST http://127.0.0.1:8787/answer \), code:bash (RAG_DOCUMENTS_DIR=docs python3 ./scripts/build-rag-index.py), code:bash (python3 ./scripts/query-rag.py "How is this node supposed to), code:bash (python3 ./scripts/rag-answer.py "What are the default model ), code:bash (RAG_CHAT_MODEL=gemma4:31b python3 ./scripts/rag-answer.py "S), code:bash (./scripts/start-rag-service.sh) (+10 more)

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (10): BaseHTTPRequestHandler, brainstorm_prompt(), capture_model(), capture_notes_dir(), capture_token(), first_line(), IdeaCaptureHandler, IdeaCaptureServer (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (12): code:bash (docker compose up -d), code:bash (curl http://OLLAMA_NODE_IP:11434/api/tags), code:bash (curl http://localhost:11434/api/tags), code:bash (docker compose up -d), code:bash (docker compose -f docker-compose.yml -f docker-compose.ollam), code:bash (curl http://localhost:11434/api/tags), code:bash (cp .env.example .env), code:bash (OLLAMA_BASE_URL=http://OLLAMA_NODE_IP:11434) (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.22
Nodes (8): Current router service, Current routing behavior, Default assignments, Model Router, Operating rules, Recommended first-pass UI defaults, TODO, UI integration target

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (8): code:bash (ollama list), Core rule, Default operating pattern, Migration and backup notes, Model roles and expected pressure, Performance Tuning, Practical tuning rules, Validation checks

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (9): code:bash (python3 ./scripts/build-rag-index.py), code:bash (./scripts/start-router-service.sh), code:bash (./scripts/check-router-connectivity.sh), code:bash (docker compose up -d), code:bash (ENABLE_OLLAMA_API=false), Open WebUI Through The Router, Recommended startup order, Router-mode Open WebUI settings (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (8): code:bash (sudo useradd --system --create-home --home-dir /var/lib/olla), code:bash (sudo mkdir -p /var/lib/ollama/.ollama/models), code:bash (sudo cp configs/ollama/ollama.service /etc/systemd/system/ol), code:bash (systemctl status ollama --no-pager), Example steps, Notes, Ollama systemd setup, Suggested host layout

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (7): Access model, Backup handling, Later hardening, Minimum baseline, Operational review points, Secrets and configuration, Security Review

### Community 12 - "Community 12"
Cohesion: 0.25
Nodes (8): Backup path examples, code:bash (./scripts/backup-ollama-store.sh), code:bash (CONFIRM_RESTORE=true ./scripts/restore-ollama-store.sh /mnt/), code:bash (BACKUP_ROOT_DIR=$HOME/local-ai-node/backups), code:bash (BACKUP_ROOT_DIR=/Volumes/MyNAS/local-ai-node-backups), code:bash (BACKUP_ROOT_DIR=/mnt/nas/local-ai-node-backups), code:bash (grep -E '^(BACKUP_ROOT_DIR|OLLAMA_HOME_DIR)=' .env), Step 5: back up or restore the Ollama model store

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (6): Base checks, Operational checks, Option A: host Ollama, Option B: Docker Ollama, Router mode, Validation Checklist

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (4): Before migration, Migration Checklist, Migration rule, On the target host

## Knowledge Gaps
- **117 isolated node(s):** `expected_optional_models`, `Planned model roles`, `code:text (.)`, `Prerequisites`, `Quick start paths` (+112 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Local AI Node` connect `Community 1` to `Community 9`, `Community 12`, `Community 6`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `generate_text()` connect `Community 0` to `Community 2`, `Community 5`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `Step 2: choose your Ollama deployment mode` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `generate_text()` (e.g. with `main()` and `answer_from_chunks()`) actually correct?**
  _`generate_text()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `build_items()` (e.g. with `iter_documents()` and `read_text_file()`) actually correct?**
  _`build_items()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `build_items()` (e.g. with `iter_documents()` and `read_text_file()`) actually correct?**
  _`build_items()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `expected_optional_models`, `Planned model roles`, `code:text (.)` to the rest of the system?**
  _117 weakly-connected nodes found - possible documentation gaps or missing edges._