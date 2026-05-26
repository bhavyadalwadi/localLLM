# Graph Report - Local-LLM  (2026-05-26)

## Corpus Check
- 34 files · ~12,568 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 347 nodes · 517 edges · 36 communities (30 shown, 6 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 76 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a7ee6a5f`
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

## God Nodes (most connected - your core abstractions)
1. `Local AI Node` - 24 edges
2. `RagRuntime` - 13 edges
3. `Model Router` - 13 edges
4. `build_chat_result()` - 12 edges
5. `classify_route()` - 11 edges
6. `RouterHandler` - 11 edges
7. `Target Host First Pass` - 11 edges
8. `Step-by-step validation scenarios` - 11 edges
9. `generate_text()` - 10 edges
10. `build_items()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `build_answer_prompt()`  [INFERRED]
  scripts/rag-answer.py → scripts/rag_lib.py
- `default_model()` --calls--> `chat_model()`  [INFERRED]
  scripts/router_service.py → scripts/rag_lib.py
- `main()` --calls--> `documents_dir()`  [INFERRED]
  scripts/rag_service.py → scripts/rag_lib.py
- `main()` --calls--> `documents_dir()`  [INFERRED]
  scripts/local_ai_runtime.py → scripts/rag_lib.py
- `main()` --calls--> `index_path()`  [INFERRED]
  scripts/rag_service.py → scripts/rag_lib.py

## Communities (36 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (35): build_items(), main(), main(), main(), build_existing_item_map(), build_index_payload(), build_items(), chat_model() (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (37): code:text (.), code:bash (./scripts/verify-ollama-models.sh), code:bash (./scripts/pull-required-models.sh), code:bash (./scripts/bootstrap-local-ai-node.sh), code:bash (EXPECT_OPTIONAL_MODELS="gemma4:31b,llava:13b" ./scripts/boot), code:bash (./scripts/preflight-target-host.sh), code:bash (RUN_SMOKE_TESTS=true ./scripts/verify-ollama-models.sh), code:bash (./scripts/pull-required-models.sh) (+29 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (26): RouterHandler, LocalAIRuntimeHandler, build_chat_result(), build_direct_response(), build_rag_response(), classify_route(), classify_route_with_images(), code_model() (+18 more)

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
Nodes (32): code:bash (./scripts/check-router-connectivity.sh), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:json ({) (+24 more)

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (8): code:bash (ollama list), Core rule, Default operating pattern, Migration and backup notes, Model roles and expected pressure, Performance Tuning, Practical tuning rules, Validation checks

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (27): Backup path examples, code:bash (./scripts/start-router-service.sh), code:bash (./scripts/start-router-rag-stack.sh), code:bash (./scripts/check-router-connectivity.sh), code:bash (curl http://127.0.0.1:8788/health), code:bash (curl -X POST http://127.0.0.1:8788/chat \), code:bash (curl -X POST http://127.0.0.1:8788/v1/chat/completions \), code:bash (python3 ./scripts/build-rag-index.py) (+19 more)

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (8): code:bash (sudo useradd --system --create-home --home-dir /var/lib/olla), code:bash (sudo mkdir -p /var/lib/ollama/.ollama/models), code:bash (sudo cp configs/ollama/ollama.service /etc/systemd/system/ol), code:bash (systemctl status ollama --no-pager), Example steps, Notes, Ollama systemd setup, Suggested host layout

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (7): Access model, Backup handling, Later hardening, Minimum baseline, Operational review points, Secrets and configuration, Security Review

### Community 12 - "Community 12"
Cohesion: 0.23
Nodes (4): RouterServer, LocalAIRuntimeServer, main(), RagRuntime

### Community 13 - "Community 13"
Cohesion: 0.25
Nodes (7): Base checks, Operational checks, Option A: host Ollama, Option B: Docker Ollama, Router mode, Scenario checks, Validation Checklist

### Community 14 - "Community 14"
Cohesion: 0.23
Nodes (6): build_answer_prompt(), answer_from_chunks(), main(), RagHandler, RagServer, rank_chunks()

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (4): Before migration, Migration Checklist, Migration rule, On the target host

## Knowledge Gaps
- **124 isolated node(s):** `expected_optional_models`, `Planned model roles`, `Screenshots`, `code:text (.)`, `Prerequisites` (+119 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Local AI Node` connect `Community 1` to `Community 9`, `Community 6`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `generate_text()` connect `Community 0` to `Community 2`, `Community 12`, `Community 5`, `Community 14`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `RagRuntime` connect `Community 12` to `Community 0`, `Community 2`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `RagRuntime` (e.g. with `LocalAIRuntimeHandler` and `LocalAIRuntimeServer`) actually correct?**
  _`RagRuntime` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `build_chat_result()` (e.g. with `.do_POST()` and `top_k()`) actually correct?**
  _`build_chat_result()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `expected_optional_models`, `Planned model roles`, `Screenshots` to the rest of the system?**
  _124 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._