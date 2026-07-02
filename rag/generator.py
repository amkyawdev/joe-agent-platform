"""Generator - Answer generation for RAG."""

from typing import List, Dict, Any, Optional, AsyncIterator

from llm.client import LLMClient
from llm.prompts import SYSTEM_PROMPT


class AnswerGenerator:
    """Generate answers using retrieved context."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
    
    def generate(
        self,
        query: str,
        context: str,
        stream: bool = False
    ) -> Any:
        """Generate answer from query and context."""
        prompt = self._build_prompt(query, context)
        
        if stream:
            return self.llm.stream(prompt)
        else:
            return self.llm.complete(prompt)
    
    def _build_prompt(self, query: str, context: str) -> str:
        """Build prompt with context."""
        return f"""Context:
{context}

Question: {query}

Based on the context above, please provide a helpful and accurate answer. 
If the context doesn't contain enough information to fully answer the question, 
say so and provide what's available."""


class RAGPipeline:
    """Complete RAG pipeline."""
    
    def __init__(
        self,
        retriever: Any,
        generator: Optional[AnswerGenerator] = None,
        llm_client: Optional[LLMClient] = None
    ):
        self.retriever = retriever
        self.generator = generator or AnswerGenerator(llm_client)
    
    def query(
        self,
        query: str,
        top_k: int = 5,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Execute complete RAG query."""
        context = self.retriever.retrieve(query, top_k=top_k)
        
        if not context:
            return {
                "query": query,
                "answer": "I couldn't find relevant information to answer your question.",
                "sources": []
            }
        
        answer = self.generator.generate(query, context, stream=stream)
        
        sources = self.retriever.search(query, top_k=top_k)
        
        return {
            "query": query,
            "answer": answer,
            "context": context,
            "sources": sources
        }
    
    def add_documents(
        self,
        texts: List[str],
        metadata: Optional[List[Dict]] = None
    ) -> None:
        """Add documents to the RAG system."""
        self.retriever.add_documents(texts, metadata)