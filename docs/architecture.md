# Architecture

## Overview

Joe-Agent-Platform is a modular AI agent platform built with the following architecture:

## Components

### CLI Module
- Command-line interface with multiple commands
- Interactive chat mode
- Web crawling and scraping
- Document analysis

### Agent Module
- **Planner**: Task decomposition and planning
- **Executor**: Task execution with tool support
- **Reasoner**: Chain-of-thought reasoning
- **Workflow**: Multi-step workflow orchestration
- **Memory**: Conversation and context management

### LLM Module
- **Client**: Unified interface for LLM interactions
- **Router**: Intelligent model routing
- **Providers**: OpenRouter and fallback providers
- **Tokenizer**: Token counting utilities

### Crawler Module
- **Browser**: Playwright-based browser automation
- **Fetcher**: HTTP and browser-based fetching
- **Parser**: HTML content parsing
- **Extractor**: Targeted content extraction
- **Cleaner**: Content cleaning and normalization

### RAG Module
- **Chunker**: Text splitting for embeddings
- **Embedding**: Text embedding generation
- **Vector Store**: ChromaDB integration
- **Retriever**: Document retrieval
- **Generator**: Answer generation

### API Module
- FastAPI-based REST API
- WebSocket support
- Authentication with JWT
- Rate limiting

## Data Flow

1. User input via CLI or API
2. Agent receives and processes input
3. LLM generates response (with optional RAG)
4. Response returned to user

## Security

- JWT authentication
- Rate limiting
- Input validation
- Secure credential handling