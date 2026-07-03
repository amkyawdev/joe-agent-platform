"""FastAPI Server - Joe AI Studio for Vercel."""

import os
from pathlib import Path
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Joe AI Studio", description="Free AI Coding Platform", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

VERCEL_ENV = os.getenv("VERCEL", "0") == "1"

# Setup Jinja2 templates
templates_dir = Path(__file__).parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request, model: str = Query(default="openrouter/free")):
    """Chat page."""
    return templates.TemplateResponse("chat.html", {"request": request, "model": model})


@app.get("/docs", response_class=HTMLResponse)
async def docs(request: Request):
    """Documentation page."""
    return templates.TemplateResponse("docs.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page."""
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/old")
async def root():
    """Legacy root endpoint."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return FileResponse(str(frontend_path))
    return {"message": "Joe AI Studio", "version": "0.1.0"}


@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "joe-ai-studio"}


@app.get("/api/models")
async def list_models():
    return {"models": [
        {"id": "openrouter/free", "name": "OpenRouter Free", "is_free": True},
        {"id": "google/gemma-4-31b-it:free", "name": "Google Gemma 4", "is_free": True},
        {"id": "cohere/north-mini-code:free", "name": "Cohere North", "is_free": True},
    ], "total": 3}


@app.get("/api/settings")
async def get_settings():
    return {"app_name": "Joe AI Studio", "default_model": "openrouter/free"}


@app.post("/api/chat")
async def chat(request: dict):
    message = request.get("message", "")
    model = request.get("model", "openrouter/free")
    history = request.get("history", [])
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    
    if not api_key:
        return {"response": f"Echo: {message}", "model": model}
    
    try:
        import httpx
        
        # Build messages with history
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
        messages.append({"role": "user", "content": message})
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://joe-ai-studio.vercel.app",
            "X-Title": "Joe AI Studio"
        }
        data = {"model": model, "messages": messages}
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=data,
                headers=headers
            )
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return {"response": result["choices"][0]["message"]["content"]}
            else:
                return {"error": result.get("error", "No response from model")}
    except Exception as e:
        return {"error": str(e)}
