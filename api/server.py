"""FastAPI Server - Main API server."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import ai, chat, crawler, search, health, settings
from api.middleware import setup_middleware
from config.settings import Settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = Settings()
    
    app = FastAPI(
        title="Joe-Agent-Platform API",
        description="AI Agent Platform with LLM, Crawler, and RAG capabilities",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    setup_middleware(app)
    
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(ai.router, prefix="/api/v1", tags=["ai"])
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
    app.include_router(crawler.router, prefix="/api/v1", tags=["crawler"])
    app.include_router(search.router, prefix="/api/v1", tags=["search"])
    app.include_router(settings.router, prefix="/api/v1", tags=["settings"])
    
    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Joe-Agent-Platform API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)