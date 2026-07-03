"""FastAPI Server - Joe AI Studio for Vercel."""

import os
from pathlib import Path
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

app = FastAPI(title="Joe AI Studio", description="Free AI Coding Platform", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

VERCEL_ENV = os.getenv("VERCEL", "0") == "1"

# Base template with shared CSS/JS
BASE_CSS = """
:root { --p: #6366f1; --bd: #12121a; --bi: #1a1a24; --tp: #fff; --ts: #a1a1aa; --br: #27272a; }
body { font-family: sans-serif; background: #0a0a0f; color: #fff; min-height: 100vh; margin: 0; }
.navbar { background: rgba(10,10,15,.9); backdrop-filter: blur(20px); border-bottom: 1px solid #27272a; padding: 1rem 0; }
.navbar-brand { font-weight: bold; font-size: 1.5rem; color: #fff; text-decoration: none; display: flex; align-items: center; gap: 0.5rem; }
.nav-link { color: #a1a1aa; text-decoration: none; padding: 0.5rem 1rem; }
.nav-link:hover, .nav-link.active { color: #fff; }
.btn-p { background: linear-gradient(135deg, #6366f1, #4f46e5); border: none; color: #fff; padding: 0.6rem 1.5rem; border-radius: 8px; font-weight: 600; text-decoration: none; display: inline-block; }
.btn-p:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(99,102,241,.3); }
.main { padding-top: 80px; }
.hero { padding: 6rem 0; text-align: center; }
.stat { font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #6366f1, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.card { background: #12121a; border: 1px solid #27272a; border-radius: 12px; padding: 1.5rem; }
.card:hover { border-color: #6366f1; transform: translateY(-4px); }
.badge-custom { background: rgba(16,185,129,.1); color: #10b981; padding: 0.25rem 0.75rem; border-radius: 100px; font-size: 0.75rem; font-weight: 600; }
.icon-box { width: 56px; height: 56px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem; font-size: 1.5rem; color: #fff; }
.chat-container { background: #12121a; border: 1px solid #27272a; border-radius: 16px; overflow: hidden; }
.msg { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.msg.user { flex-direction: row-reverse; }
.avatar { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; }
.msg.ai .avatar { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.msg.user .avatar { background: #1a1a24; }
.content { max-width: 75%; padding: 1rem 1.25rem; border-radius: 12px; }
.msg.ai .content { background: #1a1a24; border: 1px solid #27272a; }
.msg.user .content { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }
.input-field { background: #1a1a24; border: 1px solid #27272a; border-radius: 12px; padding: 0.875rem 1rem; color: #fff; resize: none; width: 100%; }
.model-btn { background: #1a1a24; border: 1px solid #27272a; color: #a1a1aa; padding: 0.375rem 0.75rem; font-size: 0.875rem; border-radius: 0.375rem; cursor: pointer; }
.model-btn:hover { border-color: #6366f1; color: #fff; }
.model-btn.active { background: #6366f1; border-color: #6366f1; color: #fff; }
.typing-indicator span { width: 8px; height: 8px; background: #a1a1aa; border-radius: 50%; animation: typing 1.4s infinite; display: inline-block; }
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing { 0%,60%,100% { transform: translateY(0); opacity: 0.4; } 30% { transform: translateY(-4px); opacity: 1; } }
footer { text-align: center; padding: 1rem; border-top: 1px solid #27272a; background: #12121a; }
code { background: #1a1a24; padding: 0.125rem 0.25rem; border-radius: 4px; }
"""

def base_page(title: str, content: str) -> str:
    """Generate base HTML page."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
<style>{BASE_CSS}</style>
</head>
<body>
<nav class="navbar">
<div class="container">
<a class="navbar-brand" href="/"><span style="width:40px;height:40px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:10px;display:flex;align-items:center;justify-content:center"><i class="bi bi-robot text-white"></i></span> Joe AI Studio</a>
<div style="display:flex;gap:1rem;align-items:center">
<a class="nav-link {'active' if title == 'Home' else ''}" href="/">Home</a>
<a class="nav-link {'active' if title == 'Chat' else ''}" href="/chat">Chat</a>
<a class="nav-link {'active' if title == 'Docs' else ''}" href="/docs">Docs</a>
<a class="nav-link {'active' if title == 'About' else ''}" href="/about">About</a>
<a href="/chat" class="btn-p"><i class="bi bi-rocket-takeoff me-1"></i> Get Started</a>
</div>
</div>
</nav>
<main class="main">{content}</main>
<footer><p style="color:#a1a1aa">&copy; 2026 Joe AI Studio. Built with OpenRouter.</p></footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    content = """
<div class="hero">
<h1 style="font-size:3rem;font-weight:800">Build with <span style="background:linear-gradient(135deg,#6366f1,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent">Free AI</span><br>Powered by OpenRouter</h1>
<p class="text-secondary mx-auto" style="max-width:600px">Generate code, chat with AI, and build applications using free coding models.</p>
<div class="mt-4"><a href="/chat" class="btn-p me-2"><i class="bi bi-chat-dots me-1"></i> Start Chatting</a><a href="/docs" class="btn" style="background:transparent;border:1px solid #27272a;color:#fff;text-decoration:none;padding:0.6rem 1.5rem;border-radius:8px"><i class="bi bi-book me-1"></i> View Docs</a></div>
<div class="d-flex justify-content-center gap-5 mt-5">
<div><div class="stat">6+</div><div class="text-secondary small">Free Models</div></div>
<div><div class="stat">1M</div><div class="text-secondary small">Max Context</div></div>
<div><div class="stat">100%</div><div class="text-secondary small">Free</div></div>
</div>
</div>
<div class="container mt-5">
<h2 class="text-center fw-bold mb-4">Free AI Models</h2>
<div class="row g-4">
<div class="col-md-6 col-lg-3"><div class="card" style="cursor:pointer" onclick="location.href='/chat?model=openrouter/free'"><div class="d-flex justify-content-between mb-2"><h5 class="mb-0">OpenRouter Free</h5><span class="badge-custom">RECOMMENDED</span></div><p class="text-secondary small mb-0">Auto-routes to best model</p></div></div>
<div class="col-md-6 col-lg-3"><div class="card" style="cursor:pointer" onclick="location.href='/chat?model=google/gemma-4-31b-it:free'"><h5 class="mb-2">Google Gemma 4</h5><span class="badge-custom">FREE</span></div></div>
<div class="col-md-6 col-lg-3"><div class="card" style="cursor:pointer" onclick="location.href='/chat?model=cohere/north-mini-code:free'"><h5 class="mb-2">Cohere North</h5><span class="badge-custom">FREE</span></div></div>
<div class="col-md-6 col-lg-3"><div class="card" style="cursor:pointer" onclick="location.href='/chat?model=nvidia/nemotron-3-ultra:free'"><h5 class="mb-2">NVIDIA Nemotron</h5><span class="badge-custom">FREE</span></div></div>
</div>
</div>
<div class="container mt-5 pb-5">
<h2 class="text-center fw-bold mb-4">Powerful Features</h2>
<div class="row g-4">
<div class="col-md-4"><div class="card"><div class="icon-box"><i class="bi bi-code-slash"></i></div><h5>Code Generation</h5><p class="text-secondary mb-0">Generate clean, efficient code.</p></div></div>
<div class="col-md-4"><div class="card"><div class="icon-box"><i class="bi bi-chat-quote"></i></div><h5>Smart Chat</h5><p class="text-secondary mb-0">Natural language conversations.</p></div></div>
<div class="col-md-4"><div class="card"><div class="icon-box"><i class="bi bi-brain"></i></div><h5>AI Reasoning</h5><p class="text-secondary mb-0">Complex problem solving.</p></div></div>
<div class="col-md-4"><div class="card"><div class="icon-box"><i class="bi bi-search"></i></div><h5>Code Review</h5><p class="text-secondary mb-0">Automated code review.</p></div></div>
<div class="col-md-4"><div class="card"><div class="icon-box"><i class="bi bi-bug"></i></div><h5>Debugging</h5><p class="text-secondary mb-0">Find and fix bugs.</p></div></div>
<div class="col-md-4"><div class="card"><div class="icon-box"><i class="bi bi-file-earmark-code"></i></div><h5>Documentation</h5><p class="text-secondary mb-0">Generate docs.</p></div></div>
</div>
</div>"""
    return HTMLResponse(content=base_page("Joe AI Studio - Free AI Coding Platform", content))


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request, model: str = Query(default="openrouter/free")):
    """Chat page."""
    content = f"""
<div class="container py-4">
<div class="chat-container">
<div style="padding:1rem 1.5rem;border-bottom:1px solid #27272a;display:flex;justify-content:space-between;align-items:center">
<div><h5 class="mb-1"><i class="bi bi-robot me-2"></i>AI Assistant</h5><small class="text-secondary">Powered by OpenRouter</small></div>
<div class="d-flex gap-2">
<button class="model-btn {'active' if model == 'openrouter/free' else ''}" onclick="setModel('openrouter/free')">Auto</button>
<button class="model-btn {'active' if model == 'google/gemma-4-31b-it:free' else ''}" onclick="setModel('google/gemma-4-31b-it:free')">Gemma</button>
<button class="model-btn {'active' if model == 'cohere/north-mini-code:free' else ''}" onclick="setModel('cohere/north-mini-code:free')">Code</button>
</div>
</div>
<div id="messages" style="height:400px;overflow-y:auto;padding:1.5rem">
<div class="msg ai"><div class="avatar"><i class="bi bi-robot text-white"></i></div><div class="content"><p class="mb-0">Hello! I am your AI coding assistant. What would you like to build?</p></div></div>
</div>
<div style="padding:1rem 1.5rem;border-top:1px solid #27272a">
<div class="d-flex gap-2">
<textarea id="input" class="input-field" rows="1" placeholder="Ask me anything..."></textarea>
<button class="btn-p" onclick="sendMessage()" style="padding:0.875rem 1rem"><i class="bi bi-send"></i></button>
<button class="btn" style="background:#1a1a24;border:1px solid #27272a;color:#a1a1aa;padding:0.875rem" onclick="clearChat()"><i class="bi bi-trash"></i></button>
</div>
</div>
</div>
</div>
<script>
let currentModel = '{model}';
let conversationHistory = [];
const inp = document.getElementById('input');
inp.addEventListener('keydown', e => {{ if(e.key==='Enter' && !e.shiftKey) {{ e.preventDefault(); sendMessage(); }} }});
inp.addEventListener('input', function() {{ this.style.height='auto'; this.style.height=Math.min(this.scrollHeight,150)+'px'; }});
function setModel(m) {{ window.location.href='/chat?model='+encodeURIComponent(m); }}
function addMsg(r,c) {{ const d=document.createElement('div'); d.className='msg '+r; const i=r==='ai'?'bi-robot':'bi-person'; const col=r==='ai'?'#fff':'#a1a1aa'; d.innerHTML='<div class="avatar"><i class="bi '+i+'" style="color:'+col+'"></i></div><div class="content"><p class="mb-0">'+c.replace(/\\n/g,'<br>')+'</p></div>'; document.getElementById('messages').appendChild(d); document.getElementById('messages').scrollTop=document.getElementById('messages').scrollHeight; }}
function typing() {{ const id='t'+Date.now(); const d=document.createElement('div'); d.id=id; d.className='msg ai'; d.innerHTML='<div class="avatar"><i class="bi bi-robot text-white"></i></div><div class="content"><div class="typing-indicator"><span></span><span></span><span></span></div></div>'; document.getElementById('messages').appendChild(d); return id; }}
function remove(id) {{ document.getElementById(id)?.remove(); }}
async function sendMessage() {{ const m=inp.value.trim(); if(!m) return; addMsg('user',m); conversationHistory.push({{role:'user',content:m}}); inp.value=''; inp.style.height='auto'; const tid=typing(); try {{ const r=await fetch('/api/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:m,model:currentModel,history:conversationHistory}})}}); const d=await r.json(); remove(tid); if(d.error) addMsg('ai','Error: '+d.error); else {{ addMsg('ai',d.response); conversationHistory.push({{role:'assistant',content:d.response}}); }} }} catch(e) {{ remove(tid); addMsg('ai','Sorry, something went wrong.'); }} }}
function clearChat() {{ document.getElementById('messages').innerHTML='<div class="msg ai"><div class="avatar"><i class="bi bi-robot text-white"></i></div><div class="content"><p class="mb-0">Chat cleared! How can I help you?</p></div></div>'; conversationHistory=[]; }}
</script>"""
    return HTMLResponse(content=base_page("Chat - Joe AI Studio", content))


@app.get("/docs", response_class=HTMLResponse)
async def docs(request: Request):
    """Docs page."""
    content = """
<div class="container py-5">
<h1 class="text-center fw-bold mb-4"><i class="bi bi-book me-2"></i>Documentation</h1>
<div class="row g-4">
<div class="col-lg-6"><div class="card"><h5><i class="bi bi-rocket-takeoff me-2" style="color:#6366f1"></i>Quick Start</h5>
<div style="background:#1a1a24;border:1px solid #27272a;border-radius:8px;padding:1rem;margin-bottom:1rem"><span style="background:#10b981;color:#fff;padding:.25rem .5rem;border-radius:4px;font-size:.75rem;font-weight:600">GET</span> <code>/api/health</code></div>
<div style="background:#1a1a24;border:1px solid #27272a;border-radius:8px;padding:1rem;margin-bottom:1rem"><span style="background:#10b981;color:#fff;padding:.25rem .5rem;border-radius:4px;font-size:.75rem;font-weight:600">GET</span> <code>/api/models</code></div>
<div style="background:#1a1a24;border:1px solid #27272a;border-radius:8px;padding:1rem"><span style="background:#10b981;color:#fff;padding:.25rem .5rem;border-radius:4px;font-size:.75rem;font-weight:600">GET</span> <code>/api/settings</code></div>
</div></div>
<div class="col-lg-6"><div class="card"><h5><i class="bi bi-chat-dots me-2" style="color:#6366f1"></i>Chat API</h5>
<div style="background:#1a1a24;border:1px solid #27272a;border-radius:8px;padding:1rem;margin-bottom:1rem"><span style="background:#f59e0b;color:#fff;padding:.25rem .5rem;border-radius:4px;font-size:.75rem;font-weight:600">POST</span> <code>/api/chat</code></div>
<p class="text-secondary small">Request: <code>{"message": "Hello!", "model": "openrouter/free"}</code></p>
</div></div>
<div class="col-lg-6"><div class="card"><h5><i class="bi bi-terminal me-2" style="color:#6366f1"></i>CLI Usage</h5>
<p class="mb-1"><code>python -m cli.main chat</code></p><p class="text-secondary small mb-2">Start interactive chat</p>
<p class="mb-1"><code>python -m cli.main code "Write a REST API"</code></p><p class="text-secondary small mb-2">Generate code</p>
</div></div>
<div class="col-lg-6"><div class="card"><h5><i class="bi bi-box me-2" style="color:#6366f1"></i>Available Models</h5>
<p class="mb-1"><code>openrouter/free</code></p><p class="text-secondary small mb-2">Auto-routes to best free model (262K context)</p>
<p class="mb-1"><code>google/gemma-4-31b-it:free</code></p><p class="text-secondary small mb-2">Google Gemma 4 (32K context)</p>
<p class="mb-1"><code>cohere/north-mini-code:free</code></p><p class="text-secondary small mb-2">Cohere North Mini (32K context)</p>
</div></div>
</div>
</div>"""
    return HTMLResponse(content=base_page("Docs - Joe AI Studio", content))


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page."""
    content = """
<div class="container py-5">
<h1 class="text-center fw-bold mb-4"><i class="bi bi-info-circle me-2"></i>About</h1>
<div class="row g-4 mb-4">
<div class="col-md-4"><div class="card text-center h-100"><i class="bi bi-currency-dollar fs-1" style="color:#10b981"></i><h5 class="mt-3">100% Free</h5><p class="text-secondary mb-0">No API costs. Powered by free models from OpenRouter.</p></div></div>
<div class="col-md-4"><div class="card text-center h-100"><i class="bi bi-shield-check fs-1" style="color:#6366f1"></i><h5 class="mt-3">Privacy First</h5><p class="text-secondary mb-0">Your conversations are private and secure.</p></div></div>
<div class="col-md-4"><div class="card text-center h-100"><i class="bi bi-lightning-charge fs-1" style="color:#f59e0b"></i><h5 class="mt-3">Fast & Reliable</h5><p class="text-secondary mb-0">Powered by modern infrastructure for quick responses.</p></div></div>
</div>
<div class="card mb-4">
<h5 class="mb-3"><i class="bi bi-stack me-2" style="color:#6366f1"></i>Technology Stack</h5>
<div class="row g-3">
<div class="col-md-3 col-6"><div class="text-center p-3" style="background:#1a1a24;border-radius:8px"><i class="bi bi-code-slash fs-4" style="color:#6366f1"></i><div class="small mt-2">Python</div></div></div>
<div class="col-md-3 col-6"><div class="text-center p-3" style="background:#1a1a24;border-radius:8px"><i class="bi bi-lightning fs-4" style="color:#10b981"></i><div class="small mt-2">FastAPI</div></div></div>
<div class="col-md-3 col-6"><div class="text-center p-3" style="background:#1a1a24;border-radius:8px"><i class="bi bi-database fs-4" style="color:#06b6d4"></i><div class="small mt-2">ChromaDB</div></div></div>
<div class="col-md-3 col-6"><div class="text-center p-3" style="background:#1a1a24;border-radius:8px"><i class="bi bi-globe fs-4" style="color:#f59e0b"></i><div class="small mt-2">OpenRouter</div></div></div>
</div>
</div>
<div class="card">
<h5 class="mb-3"><i class="bi bi-people me-2" style="color:#6366f1"></i>Features</h5>
<div class="row">
<div class="col-md-6"><ul class="list-unstyled"><li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>Code Generation</li><li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>Interactive Chat</li><li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>Web Crawling</li><li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>RAG Capabilities</li></ul></div>
<div class="col-md-6"><ul class="list-unstyled"><li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>Multiple Free Models</li><li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>CLI Interface</li><li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>REST API</li><li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>JWT Authentication</li></ul></div>
</div>
</div>
</div>"""
    return HTMLResponse(content=base_page("About - Joe AI Studio", content))


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
