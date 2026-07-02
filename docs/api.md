# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Endpoints

### Health

#### GET /health
Basic health check.

#### GET /health/detailed
Detailed health check with all services.

### AI

#### POST /ai/complete
Generate text completion.

**Request:**
```json
{
  "prompt": "Your prompt here",
  "temperature": 0.7,
  "max_tokens": 4096
}
```

**Response:**
```json
{
  "text": "Generated response"
}
```

#### POST /ai/chat
Generate chat completion.

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello"}
  ],
  "temperature": 0.7
}
```

### Crawler

#### POST /crawler/crawl
Crawl a URL and extract content.

**Request:**
```json
{
  "url": "https://example.com",
  "extract_main_content": true
}
```

### Search

#### POST /search
Search for relevant documents.

**Request:**
```json
{
  "query": "your search query",
  "top_k": 5
}
```

#### POST /search/rag
Search with RAG answer generation.