"""Retriever - Document retrieval for RAG."""

from typing import List, Dict, Any, Optional
from rag.embedding import EmbeddingGenerator
from rag.vector_store import VectorStore, ChromaVectorStore, InMemoryVectorStore


class Retriever:
    """Document retriever for RAG."""
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        embedding_generator: Optional[EmbeddingGenerator] = None,
        collection_name: str = "default"
    ):
        self.vector_store = vector_store or ChromaVectorStore(collection_name)
        self.embedding = embedding_generator or EmbeddingGenerator()
    
    def add_documents(
        self,
        texts: List[str],
        metadata: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        """Add documents to the vector store."""
        embeddings = self.embedding.generate_batch(texts)
        
        from rag.vector_store import Document
        
        documents = []
        for i, text in enumerate(texts):
            doc_id = ids[i] if ids else f"doc_{i}"
            doc_metadata = metadata[i] if metadata else {}
            
            documents.append(Document(
                id=doc_id,
                text=text,
                embedding=embeddings[i],
                metadata=doc_metadata
            ))
        
        self.vector_store.add(documents)
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Search for relevant documents."""
        query_embedding = self.embedding.generate(query)
        
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            where=filter_metadata
        )
        
        return results
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> str:
        """Retrieve and combine relevant documents."""
        results = self.search(query, top_k=top_k)
        
        if not results:
            return ""
        
        contexts = []
        for i, result in enumerate(results, 1):
            contexts.append(f"[{i}] {result['text']}")
        
        return "\n\n".join(contexts)
    
    def delete_documents(self, ids: List[str]) -> None:
        """Delete documents by ID."""
        self.vector_store.delete(ids)


class HybridRetriever(Retriever):
    """Hybrid retriever combining vector and keyword search."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyword_weight = 0.3
        self.vector_weight = 0.7
    
    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Hybrid search combining vector and keyword matching."""
        vector_results = super().search(query, top_k=top_k * 2)
        
        keyword_scores = self._keyword_search(query, vector_results)
        
        hybrid_results = []
        for result in vector_results:
            keyword_score = keyword_scores.get(result['id'], 0)
            combined_score = (
                self.vector_weight * (1 - result['distance']) +
                self.keyword_weight * keyword_score
            )
            result['score'] = combined_score
            hybrid_results.append(result)
        
        hybrid_results.sort(key=lambda x: x['score'], reverse=True)
        return hybrid_results[:top_k]
    
    def _keyword_search(
        self,
        query: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Simple keyword matching score."""
        query_terms = set(query.lower().split())
        scores = {}
        
        for doc in documents:
            text_terms = set(doc['text'].lower().split())
            intersection = query_terms & text_terms
            score = len(intersection) / len(query_terms) if query_terms else 0
            scores[doc['id']] = score
        
        return scores