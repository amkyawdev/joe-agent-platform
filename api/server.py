"""FastAPI Server - Minimal API server for Vercel."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Joe-Agent-Platform API",
    description="AI Agent Platform with Free LLM Models",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

VERCEL_ENV = os.getenv("VERCEL", "0") == "1"


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "joe-agent-platform",
        "vercel": VERCEL_ENV,
        "version": "0.1.0"
    }


@app.get("/api/models")
async def list_models():
    return {
        "models": [
            {"id": "openrouter-free", "name": "OpenRouter Free (Auto)", "is_free": True, "context_length": 262144},
            {"id": "google-gemma", "name": "Google Gemma 4", "is_free": True, "context_length": 32768},
            {"id": "cohere-north", "name": "Cohere North Mini Code", "is_free": True, "context_length": 32768},
            {"id": "nvidia-nemotron", "name": "NVIDIA Nemotron 3 Ultra", "is_free": True, "context_length": 1000000}
        ],
        "total": 4
    }


@app.get("/api/models/free")
async def list_free_models():
    return {
        "models": [
            {"id": "openrouter-free", "name": "OpenRouter Free (Auto)"},
            {"id": "google-gemma", "name": "Google Gemma 4"},
            {"id": "cohere-north", "name": "Cohere North Mini Code"},
            {"id": "nvidia-nemotron", "name": "NVIDIA Nemotron 3 Ultra"}
        ],
        "total": 4
    }


@app.get("/api/settings")
async def get_settings():
    return {
        "app_name": "Joe-Agent-Platform",
        "version": "0.1.0",
        "environment": "vercel" if VERCEL_ENV else "local",
        "default_model": "openrouter-free",
        "temperature": 0.7,
        "max_tokens": 4096
    }


@app.put("/api/settings")
async def update_settings(request: dict):
    return {"status": "success", "message": "Settings updated", "data": request}


@app.post("/api/chat")
async def chat(request: dict):
    message = request.get("message", "")
    return {
        "response": f"Echo: {message}",
        "model": "demo",
        "note": "Connect OPENROUTER_API_KEY for real AI responses"
    }


@app.post("/api/code")
async def generate_code(request: dict):
    task = request.get("task", "")
    language = request.get("language", "python")
    return {
        "code": f"# {language} code for: {task}\nprint('Hello World')",
        "language": language,
        "note": "Connect OPENROUTER_API_KEY for real code generation"
    }


@app.get("/")
async def root():
    return {
        "message": "Joe-Agent-Platform API",
        "version": "0.1.0",
        "docs": "/api/docs",
        "vercel": VERCEL_ENV
    }