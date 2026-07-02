# Joe-Agent-Platform

A comprehensive AI agent platform for building intelligent applications with LLM integration, web crawling, RAG capabilities, and more.

## Features

- 🤖 **AI Agent Framework** - Planning, execution, reasoning, and workflow management
- 🔗 **LLM Integration** - OpenRouter support with fallback providers
- 🌐 **Web Crawler** - Browser automation, parsing, and markdown conversion
- 📚 **RAG System** - Retrieval-augmented generation with vector storage
- 🚀 **REST API** - FastAPI-based API server
- 🔒 **Security** - JWT authentication, encryption, rate limiting
- 📊 **Monitoring** - Metrics, tracing, and health checks

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Docker
docker-compose up -d

# Run CLI
python -m cli.main ask "Your question here"
```

## Project Structure

- `cli/` - Command-line interface
- `agent/` - Agent core modules
- `llm/` - LLM client and providers
- `crawler/` - Web crawling utilities
- `rag/` - RAG components
- `api/` - REST API server
- `database/` - Database integrations
- `security/` - Security utilities
- `monitoring/` - Monitoring and logging

## License

MIT