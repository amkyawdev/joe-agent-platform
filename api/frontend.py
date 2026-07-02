"""Frontend API - Serve frontend and API."""

import os
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/")
async def root():
    """Serve frontend HTML."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    
    if frontend_path.exists():
        return FileResponse(str(frontend_path))
    
    return {
        "message": "Joe AI Studio API",
        "version": "0.1.0",
        "frontend": "Frontend not found. Please deploy the frontend."
    }


@router.get("/index.html")
async def index_html():
    """Serve index.html."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    
    if frontend_path.exists():
        return FileResponse(str(frontend_path))
    
    return {"error": "Frontend not found"}


@router.get("/chat")
async def chat_page():
    """Serve chat page."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    
    if frontend_path.exists():
        return FileResponse(str(frontend_path))
    
    return {"error": "Frontend not found"}


@router.get("/studio")
async def studio():
    """Redirect to root."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    
    if frontend_path.exists():
        return FileResponse(str(frontend_path))
    
    return {"message": "Joe AI Studio"}