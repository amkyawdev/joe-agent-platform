"""Vector Store - Vector storage and retrieval."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class Document:
    id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]


class VectorStore:
    """Vector storage interface."""
    
    def add(self, documents: List[Document]) -> None:
        """Add documents to the store."""
        raise NotImplementedError
    
    def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        raise NotImplementedError
    
    def delete(self, ids: List[str]) -> None:
        """Delete documents by ID."""
        raise NotImplementedError
    
    def get(self, id: str) -> Optional[Document]:
        """Get document by ID."""
        raise NotImplementedError


class ChromaVectorStore(VectorStore):
    """ChromaDB-based vector store."""
    
    def __init__(self, collection_name: str = "default", persist_directory: Optional[str] = None):
        self.collection_name = collection_name
        self.persist_directory = persist_directory or "storage/vectors"
        self._client = None
        self._collection = None
    
    def _get_client(self):
        """Get or create Chroma client."""
        if self._client is None:
            import chromadb
            from chromadb.config import Settings
            
            self._client = chromadb.Client(Settings(
                persist_directory=self.persist_directory,
                anonymized_telemetry=False
            ))
            
            self._collection = self._client.get_or_create_collection(
                name=self.collection_name
            )
        
        return self._client, self._collection
    
    def add(self, documents: List[Document]) -> None:
        """Add documents to Chroma."""
        _, collection = self._get_client()
        
        collection.add(
            ids=[doc.id for doc in documents],
            embeddings=[doc.embedding for doc in documents],
            documents=[doc.text for doc in documents],
            metadatas=[doc.metadata for doc in documents]
        )
    
    def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 5,
        where: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Search Chroma collection."""
        _, collection = self._get_client()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )
        
        documents = []
        for i in range(len(results['ids'][0])):
            documents.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else 0,
                'metadata': results['metadatas'][0][i] if 'metadatas' in results else {}
            })
        
        return documents
    
    def delete(self, ids: List[str]) -> None:
        """Delete documents from Chroma."""
        _, collection = self._get_client()
        collection.delete(ids=ids)
    
    def get(self, id: str) -> Optional[Document]:
        """Get document by ID."""
        _, collection = self._get_client()
        
        results = collection.get(ids=[id])
        if results['ids']:
            return Document(
                id=results['ids'][0],
                text=results['documents'][0],
                embedding=results['embeddings'][0] if 'embeddings' in results else [],
                metadata=results['metadatas'][0] if 'metadatas' in results else {}
            )
        return None


class InMemoryVectorStore(VectorStore):
    """In-memory vector store for testing."""
    
    def __init__(self):
        self.documents: Dict[str, Document] = {}
    
    def add(self, documents: List[Document]) -> None:
        """Add documents to memory."""
        for doc in documents:
            self.documents[doc.id] = doc
    
    def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search in-memory documents."""
        similarities = []
        
        for doc_id, doc in self.documents.items():
            similarity = self._cosine_similarity(query_embedding, doc.embedding)
            similarities.append((doc_id, doc, similarity))
        
        similarities.sort(key=lambda x: x[2], reverse=True)
        
        return [
            {
                'id': doc_id,
                'text': doc.text,
                'distance': 1 - sim,
                'metadata': doc.metadata
            }
            for doc_id, doc, sim in similarities[:top_k]
        ]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity."""
        import numpy as np
        
        a = np.array(a)
        b = np.array(b)
        
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0
        
        return dot / (norm_a * norm_b)
    
    def delete(self, ids: List[str]) -> None:
        """Delete documents from memory."""
        for id in ids:
            self.documents.pop(id, None)
    
    def get(self, id: str) -> Optional[Document]:
        """Get document from memory."""
        return self.documents.get(id)