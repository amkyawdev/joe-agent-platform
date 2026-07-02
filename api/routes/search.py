"""Search Routes - RAG search endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_retriever, get_rag_pipeline
from api.schemas import SearchRequest, SearchResponse, SearchResult
from rag.retriever import Retriever, RAGPipeline


router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    retriever: Retriever = Depends(get_retriever)
) -> SearchResponse:
    """Search for relevant documents."""
    try:
        results = retriever.search(
            query=request.query,
            top_k=request.top_k
        )
        
        search_results = [
            SearchResult(
                text=r['text'],
                score=r.get('distance', r.get('score', 0)),
                metadata=r.get('metadata', {})
            )
            for r in results
        ]
        
        return SearchResponse(
            query=request.query,
            results=search_results,
            total=len(search_results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/rag")
async def rag_search(
    request: SearchRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
) -> dict:
    """Search with RAG and answer generation."""
    try:
        result = pipeline.query(
            query=request.query,
            top_k=request.top_k
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/index")
async def index_documents(
    texts: List[str],
    metadata: Optional[List[dict]] = None
) -> dict:
    """Index documents for search."""
    try:
        retriever: Retriever = Depends(get_retriever)
        retriever.add_documents(texts, metadata)
        return {
            "status": "success",
            "indexed": len(texts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))