# Graph Report - Local-LLM  (2026-05-26)

## Corpus Check
- 53 files · ~15,138 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 469 nodes · 621 edges · 59 communities (44 shown, 15 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 76 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1df2c54c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

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
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]

## God Nodes (most connected - your core abstractions)
1. `Local AI Node` - 24 edges
2. `Local-LLM Project Context` - 16 edges
3. `Router Runtime` - 15 edges
4. `Base Node` - 15 edges
5. `Model Router` - 15 edges
6. `Local-LLM Architecture` - 14 edges
7. `RagRuntime` - 13 edges
8. `build_chat_result()` - 12 edges
9. `classify_route()` - 11 edges
10. `RouterHandler` - 11 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `top_k()`  [INFERRED]
  scripts/rag-answer.py → scripts/rag_lib.py
- `main()` --calls--> `top_k()`  [INFERRED]
  scripts/query-rag.py → scripts/rag_lib.py
- `default_model()` --calls--> `chat_model()`  [INFERRED]
  scripts/router_service.py → scripts/rag_lib.py
- `main()` --calls--> `documents_dir()`  [INFERRED]
  scripts/rag_service.py → scripts/rag_lib.py
- `main()` --calls--> `index_path()`  [INFERRED]
  scripts/rag_service.py → scripts/rag_lib.py

## Communities (59 total, 15 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (38): build_items(), main(), main(), main(), main(), build_answer_prompt(), build_existing_item_map(), build_index_payload() (+30 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (15): code:text (.), Future work, How This Actually Works, License, LLM Start Here, Local AI Node, No-Docker note, Notes on migration (+7 more)

### Community 2 - "Community 2"
Cohesion: 0.1
Nodes (29): RouterHandler, RouterServer, LocalAIRuntimeHandler, LocalAIRuntimeServer, top_k(), build_chat_result(), build_direct_response(), build_rag_response() (+21 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (23): 1. Clone the repo, 2. Create the environment file, 3. Confirm Ollama is installed and healthy on the host, 4. Run repo preflight, 5. Pull, restore, or verify the model inventory, 5. Validate or restore the model inventory, 6. Start Open WebUI, 7. Validate the stack (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (18): Build the index, code:bash (python3 ./scripts/build-rag-index.py), code:bash (curl -X POST http://127.0.0.1:8787/answer \), code:bash (RAG_DOCUMENTS_DIR=docs python3 ./scripts/build-rag-index.py), code:bash (python3 ./scripts/query-rag.py "How is this node supposed to), code:bash (python3 ./scripts/rag-answer.py "What are the default model ), code:bash (RAG_CHAT_MODEL=gemma4:31b python3 ./scripts/rag-answer.py "S), code:bash (./scripts/start-rag-service.sh) (+10 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (11): BaseHTTPRequestHandler, brainstorm_prompt(), capture_model(), capture_notes_dir(), capture_token(), first_line(), IdeaCaptureHandler, IdeaCaptureServer (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (12): code:bash (docker compose up -d), code:bash (curl http://OLLAMA_NODE_IP:11434/api/tags), code:bash (curl http://localhost:11434/api/tags), code:bash (docker compose up -d), code:bash (docker compose -f docker-compose.yml -f docker-compose.ollam), code:bash (curl http://localhost:11434/api/tags), code:bash (cp .env.example .env), code:bash (OLLAMA_BASE_URL=http://OLLAMA_NODE_IP:11434) (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (34): code:bash (./scripts/check-router-connectivity.sh), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:json ({) (+26 more)

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (8): code:bash (ollama list), Core rule, Default operating pattern, Migration and backup notes, Model roles and expected pressure, Performance Tuning, Practical tuning rules, Validation checks

### Community 9 - "Community 9"
Cohesion: 0.21
Nodes (12): Backup path examples, code:bash (docker compose up -d), code:bash (./scripts/check-open-webui-connectivity.sh), code:text (http://localhost:3000), code:bash (./scripts/backup-ollama-store.sh), code:bash (CONFIRM_RESTORE=true ./scripts/restore-ollama-store.sh /mnt/), code:bash (BACKUP_ROOT_DIR=$HOME/local-ai-node/backups), code:bash (BACKUP_ROOT_DIR=/Volumes/MyNAS/local-ai-node-backups) (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (8): code:bash (sudo useradd --system --create-home --home-dir /var/lib/olla), code:bash (sudo mkdir -p /var/lib/ollama/.ollama/models), code:bash (sudo cp configs/ollama/ollama.service /etc/systemd/system/ol), code:bash (systemctl status ollama --no-pager), Example steps, Notes, Ollama systemd setup, Suggested host layout

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (7): Access model, Backup handling, Later hardening, Minimum baseline, Operational review points, Secrets and configuration, Security Review

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (16): Business Purpose, Critical Dependencies, Current Architecture Themes, Deployment Model, Environments, Important APIs, Important Databases, Important Queues / Events (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.25
Nodes (7): Base checks, Operational checks, Option A: host Ollama, Option B: Docker Ollama, Router mode, Scenario checks, Validation Checklist

### Community 14 - "Community 14"
Cohesion: 0.27
Nodes (4): main(), RagHandler, RagServer, rank_chunks()

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (4): Before migration, Migration Checklist, Migration rule, On the target host

### Community 36 - "Community 36"
Cohesion: 0.12
Nodes (15): Base Node, Critical Workflows, Dangerous Code Paths, Databases Used, Dependencies, Failure Modes, Important Source Files, Inbound APIs (+7 more)

### Community 37 - "Community 37"
Cohesion: 0.12
Nodes (15): Critical Workflows, Dangerous Code Paths, Databases Used, Dependencies, Failure Modes, Important Source Files, Inbound APIs, Known Technical Debt (+7 more)

### Community 38 - "Community 38"
Cohesion: 0.13
Nodes (14): Auth Flow, Caching Layers, Deployment Topology, End-to-End Request Flows, Event-Driven Architecture, Failover Behavior, Frontend / Backend Interaction, Local-LLM Architecture (+6 more)

### Community 39 - "Community 39"
Cohesion: 0.18
Nodes (10): Debugging, Deployment, Feature Rollout, Incident Response, Local Development, Local-LLM Workflows, Migrations, Observability Investigation (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.2
Nodes (9): API Conventions, Architecture Patterns, Database / Migration Patterns, Error Handling / Logging, Local-LLM Coding Rules, Naming / Structure, State Management, Testing Conventions (+1 more)

### Community 41 - "Community 41"
Cohesion: 0.22
Nodes (10): code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (python3 ./scripts/build-rag-index.py), code:bash (./scripts/start-local-ai-runtime.sh), code:bash (./scripts/start-router-rag-stack.sh), code:bash (./scripts/check-router-connectivity.sh), code:bash (ENABLE_OLLAMA_API=false), Open WebUI Through The Router, Recommended startup order (+2 more)

### Community 42 - "Community 42"
Cohesion: 0.22
Nodes (9): code:bash (RUN_SMOKE_TESTS=true ./scripts/verify-ollama-models.sh), code:bash (./scripts/pull-required-models.sh), code:bash (OPTIONAL_MODELS="gemma4:31b" ./scripts/pull-required-models.), code:bash (OPTIONAL_MODELS="qwen3:30b" ./scripts/pull-required-models.s), code:bash (./scripts/show-model-files.sh gemma4:31b), code:bash (python3 ./scripts/build-rag-index.py), code:bash (python3 ./scripts/query-rag.py "What models are part of the ), Download models on a new system (+1 more)

### Community 43 - "Community 43"
Cohesion: 0.25
Nodes (9): code:bash (python3 ./scripts/rag-answer.py "What is the deployment flow), code:bash (./scripts/start-router-service.sh), code:bash (./scripts/start-local-ai-runtime.sh), code:bash (./scripts/start-router-rag-stack.sh), code:bash (./scripts/check-router-connectivity.sh), code:bash (curl http://127.0.0.1:8788/health), code:bash (curl -X POST http://127.0.0.1:8788/chat \), Open WebUI Relationship (+1 more)

### Community 44 - "Community 44"
Cohesion: 0.29
Nodes (6): Critical Entrypoints, First Read, How To Start Reasoning, Local-LLM Onboarding, Local Run Baseline, Module Map

### Community 45 - "Community 45"
Cohesion: 0.33
Nodes (6): code:bash (./scripts/verify-ollama-models.sh), code:bash (./scripts/pull-required-models.sh), code:bash (./scripts/bootstrap-local-ai-node.sh), code:bash (EXPECT_OPTIONAL_MODELS="gemma4:31b,llava:13b" ./scripts/boot), code:bash (./scripts/preflight-target-host.sh), Step 3: verify the model inventory

### Community 46 - "Community 46"
Cohesion: 0.4
Nodes (4): Graphify-first repo discovery, Local-LLM Decision Log, Preserve repo separation, Router remains an add-on to a stable base node

### Community 47 - "Community 47"
Cohesion: 0.5
Nodes (3): Critical Entrypoints, Read First, Top-Level Modules

### Community 48 - "Community 48"
Cohesion: 0.67
Nodes (3): code:bash (cp .env.example .env), code:bash (cp .env.staging.example .env), Step 1: prepare the environment

## Knowledge Gaps
- **218 isolated node(s):** `expected_optional_models`, `Planned model roles`, `Screenshots`, `code:text (.)`, `Prerequisites` (+213 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Local AI Node` connect `Community 1` to `Community 6`, `Community 41`, `Community 42`, `Community 43`, `Community 9`, `Community 45`, `Community 48`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `generate_text()` connect `Community 0` to `Community 2`, `Community 5`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `RagRuntime` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **What connects `expected_optional_models`, `Planned model roles`, `Screenshots` to the rest of the system?**
  _218 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._