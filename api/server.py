"""FastAPI Server - Main API server for Vercel."""

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

# Detect Vercel environment
VERCEL_ENV = os.getenv("VERCEL", "0") == "1"


# ==================== HEALTH ====================

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "joe-agent-platform",
        "vercel": VERCEL_ENV,
        "version": "0.1.0"
    }


# ==================== MODELS ====================

@app.get("/api/models")
async def list_models():
    from llm.models import AVAILABLE_MODELS
    models = []
    for model_id, config in AVAILABLE_MODELS.items():
        models.append({
            "id": model_id,
            "name": config.get("name", model_id),
            "is_free": config.get("is_free", False),
            "context_length": config.get("context_length", 4096),
            "capabilities": config.get("capabilities", [])
        })
    return {"models": models, "total": len(models)}


@app.get("/api/models/free")
async def list_free_models():
    from llm.models import AVAILABLE_MODELS
    free_models = [
        {"id": model_id, "name": config.get("name", model_id)}
        for model_id, config in AVAILABLE_MODELS.items()
        if config.get("is_free", False)
    ]
    return {"models": free_models, "total": len(free_models)}


# ==================== SETTINGS ====================

@app.get("/api/settings")
async def get_settings():
    return {
        "app_name": "Joe-Agent-Platform",
        "version": "0.1.0",
        "environment": "vercel" if VERCEL_ENV else "local",
        "default_model": "openrouter-free",
        "temperature": 0.7,
        "max_tokens": 4096,
        "features": {
            "llm": True,
            "crawler": True,
            "rag": True
        }
    }


@app.put("/api/settings")
async def update_settings(request: dict):
    return {
        "status": "success",
        "message": "Settings updated",
        "data": request
    }


# ==================== CHAT ====================

@app.post("/api/chat")
async def chat(request: dict):
    message = request.get("message", "")
    model = request.get("model", "openrouter-free")
    
    try:
        from llm.client import LLMClient
        client = LLMClient(model=model)
        response = client.chat([{"role": "user", "content": message}])
        return {"response": response, "model": model}
    except Exception as e:
        return {"error": str(e), "message": "Chat failed"}


# ==================== CODE ====================

@app.post("/api/code")
async def generate_code(request: dict):
    task = request.get("task", "")
    language = request.get("language", "python")
    model = request.get("model", "openrouter-free")
    
    try:
        from llm.client import LLMClient
        client = LLMClient(model=model)
        prompt = f"Generate {language} code for: {task}"
        response = client.complete(prompt)
        return {"code": response, "language": language}
    except Exception as e:
        return {"error": str(e), "message": "Code generation failed"}


# ==================== ROOT ====================

@app.get("/")
async def root():
    return {
        "message": "Joe-Agent-Platform API",
        "version": "0.1.0",
        "docs": "/api/docs",
        "vercel": VERCEL_ENV
    }