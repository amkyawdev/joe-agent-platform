# Joe-Agent-Platform

> AI Agent Platform with Free LLM Coding Models

Build intelligent applications with LLM integration, web crawling, RAG capabilities, and powerful CLI tools — all using **free AI models**.

---

## ✨ Features

| Module | Description |
|--------|-------------|
| **CLI** | 12 commands: ask, chat, code, crawl, scrape, search, summarize, analyze |
| **Agent** | Planner, executor, reasoning, workflow, memory, tools |
| **LLM** | OpenRouter integration with 6+ free coding models |
| **Crawler** | Playwright browser automation, parsing, markdown |
| **RAG** | ChromaDB vector store, embeddings, retrieval |
| **API** | FastAPI server with WebSocket, JWT auth, rate limiting |

---

## 🚀 Quick Start

```bash
# Clone & install
pip install -r requirements.txt

# Run code generation
python -m cli.main code "Write a REST API in Python"

# Interactive chat
python -m cli.main chat

# List free models
python -m cli.main models --free-only

# Run API server
uvicorn api.server:app --port 8000
```

---

## ⭐ Free Models

| Model | Context | Best For |
|-------|---------|----------|
| `openrouter/free` | 262K | Auto-routes to best free model |
| `google/gemma-4-31b-it:free` | 32K | General coding |
| `cohere/north-mini-code:free` | 32K | Fast code generation |
| `nvidia/nemotron-3-ultra:free` | 1M | Long context tasks |

---

## 📁 Project Structure

```
joe-agent-platform/
├── cli/          # Command-line interface
├── agent/        # AI agent framework
├── llm/          # LLM providers & models
├── crawler/      # Web crawling
├── rag/          # RAG system
├── api/          # FastAPI server
├── database/     # DB integrations
├── security/     # JWT, rate limiting
└── tests/        # Unit tests (28 passing)
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

---

## 📄 License

MIT