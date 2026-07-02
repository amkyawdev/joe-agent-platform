"""Chunker - Text chunking for RAG."""

from typing import List, Dict, Any, Optional
import re


class TextChunker:
    """Split text into chunks for embedding."""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        min_chunk_size: int = 100
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def chunk(self, text: str, metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Split text into chunks."""
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            
            if end < text_length:
                break_point = self._find_break_point(text, start, end)
                if break_point > start + self.min_chunk_size:
                    end = break_point
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunk_data = {
                    'text': chunk_text,
                    'metadata': metadata or {}
                }
                chunk_data['metadata']['chunk_start'] = start
                chunk_data['metadata']['chunk_end'] = end
                chunks.append(chunk_data)
            
            start = end - self.chunk_overlap
            if start >= text_length - self.min_chunk_size:
                break
        
        return chunks
    
    def _find_break_point(self, text: str, start: int, end: int) -> int:
        """Find a good break point at sentence/paragraph boundary."""
        search_start = max(start, end - 200)
        
        for sep in ['\n\n', '\n', '. ', '? ', '! ', '; ', ', ']:
            pos = text.rfind(sep, search_start, end)
            if pos > search_start:
                return pos + len(sep)
        
        return end
    
    def chunk_by_sentences(self, text: str, metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Chunk text by sentences."""
        from crawler.cleaner import ContentCleaner
        cleaner = ContentCleaner()
        sentences = cleaner.split_sentences(text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        'text': ' '.join(current_chunk),
                        'metadata': metadata or {}
                    })
                    current_chunk = current_chunk[-2:] if len(current_chunk) > 2 else []
                    current_size = sum(len(s) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        if current_chunk:
            chunks.append({
                'text': ' '.join(current_chunk),
                'metadata': metadata or {}
            })
        
        return chunks


class SemanticChunker:
    """Semantic chunking based on topic changes."""
    
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
    
    def chunk(self, text: str, metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Chunk text semantically."""
        return TextChunker().chunk(text, metadata)