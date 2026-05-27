# Local-LLM Graph Relationships

       ## Service Dependency Graph
       Local-LLM
-> Open WebUI + Ollama node
-> OpenAI-compatible router service
-> optional RAG indexing/runtime path
-> API: `POST /chat`
-> API: `GET /v1/models`
-> API: `POST /v1/chat/completions`
-> Async: routing decisions
-> Async: RAG indexing/build jobs
-> Async: model inventory/bootstrap scripts
-> Deployment: Docker-based local AI node, with single-process router+RAG runtime available through startup scripts.

       ## Runtime Dependency Graph
       Local-LLM
-> Runtime: Docker
-> Runtime: Shell
-> Runtime: Ollama
-> Runtime: Open WebUI
-> Runtime: Docker Compose

       ## Database Relationship Graph
       Local-LLM
-> no dedicated database visible

       ## API Consumer / Provider Graph
       Local-LLM
-> `POST /chat`
-> `GET /v1/models`
-> `POST /v1/chat/completions`

       ## Queue Publisher / Consumer Graph
       Local-LLM
-> routing decisions
-> RAG indexing/build jobs
-> model inventory/bootstrap scripts

       ## Shared Package Dependency Graph
       Local-LLM
-> no notable shared package layer beyond app-local dependencies

       ## Deployment Relationship Graph
       Local-LLM
       - Docker-based local AI node, with single-process router+RAG runtime available through startup scripts.

       ## Cross-Repo Relationship Graph
       Local-LLM
-> sleep-to-plan (can consume the router endpoint instead of direct Ollama)
-> docker-powerhouse (natural homelab host for the stack)
