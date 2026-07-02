# Developer Guide

## Setup

```bash
git clone <repo>
cd Joe-Agent-Platform
pip install -r requirements.txt
pip install -r requirements-dev.txt  # dev dependencies
```

## Development

### Running Locally

```bash
uvicorn api.server:app --reload
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Style

We use:
- Black for formatting
- Ruff for linting
- MyPy for type checking

```bash
black .
ruff check .
mypy .
```

## Adding New Commands

1. Create command in `cli/commands/`
2. Add to `cli/main.py`
3. Add tests in `tests/cli/`

## Adding New API Routes

1. Create route file in `api/routes/`
2. Add schema in `api/schemas/`
3. Register in `api/server.py`

## Adding New LLM Providers

1. Create provider class in `llm/providers/`
2. Register in `llm/router.py`
3. Update `llm/models.py`