"""Cleaner - Content cleaning utilities."""

import re
from typing import Optional


class ContentCleaner:
    """Clean and normalize extracted content."""
    
    def __init__(self):
        self.whitespace_pattern = re.compile(r'\s+')
        self.url_pattern = re.compile(r'https?://\S+')
        self.email_pattern = re.compile(r'\S+@\S+\.\S+')
    
    def clean(self, text: str) -> str:
        """Clean text content."""
        if not text:
            return ""
        
        text = self.remove_html_tags(text)
        text = self.normalize_whitespace(text)
        text = self.remove_extra_newlines(text)
        text = self.clean_special_characters(text)
        
        return text.strip()
    
    def remove_html_tags(self, text: str) -> str:
        """Remove HTML tags from text."""
        clean = re.sub(r'<[^>]+>', '', text)
        return clean
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace."""
        return self.whitespace_pattern.sub(' ', text)
    
    def remove_extra_newlines(self, text: str) -> str:
        """Remove extra newlines."""
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text
    
    def clean_special_characters(self, text: str) -> str:
        """Clean special characters."""
        text = text.replace('\xa0', ' ')
        text = text.replace('\u200b', '')
        text = text.replace('\ufeff', '')
        return text
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return self.url_pattern.sub('[URL]', text)
    
    def remove_emails(self, text: str) -> str:
        """Remove email addresses."""
        return self.email_pattern.sub('[EMAIL]', text)
    
    def truncate(self, text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to maximum length."""
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    def split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        sentence_endings = re.compile(r'(?<=[.!?])\s+')
        sentences = sentence_endings.split(text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_numbers(self, text: str) -> list[str]:
        """Extract all numbers from text."""
        return re.findall(r'\d+\.?\d*', text)
    
    def count_words(self, text: str) -> int:
        """Count words in text."""
        words = re.findall(r'\b\w+\b', text)
        return len(words)