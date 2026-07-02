"""Extractor - Content extraction utilities."""

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import re


class ContentExtractor:
    """Extract specific content from HTML."""
    
    def __init__(self):
        self.selectors = {
            'article': ['article', 'main', '[role="main"]'],
            'content': ['.content', '#content', '.post', '.article'],
            'comments': ['.comments', '#comments', '.disqus'],
            'sidebar': ['aside', '.sidebar', '#sidebar']
        }
    
    def extract_by_selector(self, html: str, selector: str) -> str:
        """Extract content using CSS selector."""
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.select(selector)
        
        if not elements:
            return ""
        
        return '\n\n'.join(el.get_text(strip=True) for el in elements)
    
    def extract_by_query(self, html: str, query: str) -> str:
        """Extract content based on natural language query."""
        soup = BeautifulSoup(html, 'lxml')
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['title', 'heading', 'header']):
            for tag in ['h1', 'h2', '.title', '.heading']:
                elements = soup.select(tag)
                if elements:
                    return '\n'.join(el.get_text(strip=True) for el in elements)
        
        if any(word in query_lower for word in ['link', 'url', 'website']):
            links = soup.find_all('a', href=True)
            return '\n'.join(f"{a.get_text(strip=True)}: {a['href']}" for a in links[:20])
        
        return self.extract_main_content(html)
    
    def extract_all_text(self, html: str) -> str:
        """Extract all readable text."""
        soup = BeautifulSoup(html, 'lxml')
        
        for tag in ['script', 'style', 'nav', 'footer', 'header']:
            for element in soup.find_all(tag):
                element.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        return '\n\n'.join(lines)
    
    def extract_main_content(self, html: str) -> str:
        """Extract main article content."""
        soup = BeautifulSoup(html, 'lxml')
        
        article = soup.find('article')
        if article:
            return article.get_text(separator='\n', strip=True)
        
        main = soup.find('main')
        if main:
            return main.get_text(separator='\n', strip=True)
        
        content_selectors = ['.content', '#content', '.post', '.article', '.entry']
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                return content.get_text(separator='\n', strip=True)
        
        return self.extract_all_text(html)
    
    def extract_structured_data(self, html: str) -> List[Dict[str, Any]]:
        """Extract structured data (JSON-LD, Microdata)."""
        soup = BeautifulSoup(html, 'lxml')
        data = []
        
        json_ld = soup.find_all('script', type='application/ld+json')
        for script in json_ld:
            try:
                import json
                data.append(json.loads(script.string))
            except Exception:
                pass
        
        return data