"""Chroma - ChromaDB vector database integration."""

from typing import List, Dict, Any, Optional


class ChromaClient:
    """ChromaDB client wrapper."""
    
    def __init__(self, persist_directory: str = "storage/vectors"):
        self.persist_directory = persist_directory
        self._client = None
        self._collections: Dict[str, Any] = {}
    
    def _get_client(self):
        """Get or create Chroma client."""
        if self._client is None:
            import chromadb
            from chromadb.config import Settings
            
            self._client = chromadb.Client(Settings(
                persist_directory=self.persist_directory,
                anonymized_telemetry=False
            ))
        
        return self._client
    
    def get_or_create_collection(self, name: str) -> Any:
        """Get or create a collection."""
        if name not in self._collections:
            client = self._get_client()
            self._collections[name] = client.get_or_create_collection(name)
        return self._collections[name]
    
    def add(
        self,
        collection_name: str,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadata: Optional[List[Dict]] = None
    ) -> None:
        """Add documents to collection."""
        collection = self.get_or_create_collection(collection_name)
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata
        )
    
    def query(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 10,
        where: Optional[Dict] = None
    ) -> Dict[str, List]:
        """Query collection."""
        collection = self.get_or_create_collection(collection_name)
        return collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
    
    def delete(self, collection_name: str, ids: List[str]) -> None:
        """Delete documents from collection."""
        collection = self.get_or_create_collection(collection_name)
        collection.delete(ids=ids)