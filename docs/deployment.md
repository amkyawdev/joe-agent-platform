# Deployment

## Docker

### Build Image

```bash
docker build -t joe-agent-platform:latest .
```

### Run with Docker Compose

```bash
docker-compose up -d
```

### Environment Variables

Set these in your `.env` file:

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
OPENROUTER_API_KEY=your-api-key
SECRET_KEY=your-secret-key
```

## Production

### Requirements

- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- ChromaDB
- OpenRouter API key

### Steps

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Run migrations
5. Start the server: `uvicorn api.server:app --host 0.0.0.0 --port 8000`

## Kubernetes

See `kubernetes/` directory for K8s manifests.