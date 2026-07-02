"""Embedding - Text embedding utilities."""

from typing import List, Optional, Any
import numpy as np


class EmbeddingGenerator:
    """Generate text embeddings."""
    
    def __init__(self, model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model
        self._model = None
    
    def _load_model(self):
        """Lazy load embedding model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                self._model = self._mock_embedding
    
    def generate(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        self._load_model()
        if callable(self._model):
            return self._model([text])[0]
        
        embedding = self._model.encode(text)
        return embedding.tolist()
    
    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        self._load_model()
        
        if callable(self._model):
            return self._model(texts)
        
        embeddings = self._model.encode(texts)
        return embeddings.tolist()
    
    def _mock_embedding(self, texts: List[str]) -> List[List[float]]:
        """Mock embeddings for testing."""
        dim = 384
        np.random.seed(42)
        return [np.random.randn(dim).tolist() for _ in texts]
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return 384


class OpenAIEmbedding(EmbeddingGenerator):
    """OpenAI-compatible embedding generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-ada-002"):
        super().__init__(model)
        self.api_key = api_key
        self.dimension = 1536
    
    def generate(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API."""
        import httpx
        import os
        
        api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return super().generate(text)
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    "https://api.openai.com/v1/embeddings",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "input": text,
                        "model": self.model_name
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["data"][0]["embedding"]
        except Exception:
            return super().generate(text)


class LocalEmbedding(EmbeddingGenerator):
    """Local embedding model using transformers."""
    
    def __init__(self, model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        super().__init__(model)
        self.dimension = 384
    
    def _load_model(self):
        """Load local embedding model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
                self.dimension = self._model.get_sentence_embedding_dimension()
            except ImportError:
                self._model = self._mock_embedding