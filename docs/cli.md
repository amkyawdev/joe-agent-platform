# CLI Documentation

## Installation

```bash
pip install -r requirements.txt
```

## Commands

### ask
Ask a question to the AI agent.

```bash
python -m cli.main ask "What is AI?"
```

Options:
- `--model, -m`: LLM model to use
- `--temperature, -t`: Sampling temperature
- `--stream`: Stream response

### chat
Interactive chat session.

```bash
python -m cli.main chat
```

Options:
- `--model, -m`: LLM model to use
- `--system, -s`: System prompt
- `--history`: Number of history messages

### crawl
Crawl a website.

```bash
python -m cli.main crawl https://example.com
```

Options:
- `--depth, -d`: Crawl depth
- `--output, -o`: Output file
- `--markdown`: Convert to markdown

### scrape
Scrape content from a URL.

```bash
python -m cli.main scrape https://example.com --selector "article"
```

Options:
- `--selector, -s`: CSS selector
- `--query, -q`: Natural language query
- `--format, -f`: Output format (text/json/html)

### search
Search using RAG.

```bash
python -m cli.main search "your query"
```

Options:
- `--top-k, -k`: Number of results
- `--collection, -c`: Vector collection name

### summarize
Summarize a document.

```bash
python -m cli.main summarize document.txt
```

Options:
- `--length, -l`: Summary length (short/medium/long)
- `--format, -f`: Format (bullet/paragraph)

### config
Manage configuration.

```bash
python -m cli.main config --list
python -m cli.main config --get LLM_MODEL
python -m cli.main config --set LLM_MODEL gpt-4
```

### models
List available LLM models.

```bash
python -m cli.main models
python -m cli.main models --provider openrouter
```

### health
Check system health.

```bash
python -m cli.main health
python -m cli.main health --detailed
```