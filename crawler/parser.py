"""Parser - HTML and content parsing."""

from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class ParsedContent:
    title: str
    text: str
    links: List[str]
    images: List[str]
    metadata: Dict[str, str]
    html: str


class HTMLParser:
    """Parse HTML content."""
    
    def __init__(self):
        self.ignored_tags = ['script', 'style', 'nav', 'footer', 'header', 'aside']
        self.important_tags = ['article', 'main', 'section', 'div']
    
    def parse(self, html: str, url: str = "") -> ParsedContent:
        """Parse HTML content."""
        soup = BeautifulSoup(html, 'lxml')
        
        title = self._extract_title(soup)
        text = self._extract_text(soup)
        links = self._extract_links(soup, url)
        images = self._extract_images(soup)
        metadata = self._extract_metadata(soup)
        
        return ParsedContent(
            title=title,
            text=text,
            links=links,
            images=images,
            metadata=metadata,
            html=html
        )
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        if soup.title:
            return soup.title.string or ""
        
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        meta = soup.find('meta', property='og:title')
        if meta and meta.get('content'):
            return meta['content']
        
        return ""
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract main text content."""
        for tag in self.ignored_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        main_content = soup.find('main') or soup.find('article') or soup.body or soup
        
        text_parts = []
        for element in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th']):
            text = element.get_text(strip=True)
            if text:
                text_parts.append(text)
        
        return '\n\n'.join(text_parts)
    
    def _extract_links(self, soup: BeautifulSoup, base: str) -> List[str]:
        """Extract links from content."""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith(('http://', 'https://', '/')):
                links.append(href)
        return links[:100]
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract image URLs."""
        images = []
        for img in soup.find_all('img', src=True):
            images.append(img['src'])
        return images[:50]
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata."""
        metadata = {}
        
        meta_tags = [
            ('description', 'meta[name="description"]', 'content'),
            ('keywords', 'meta[name="keywords"]', 'content'),
            ('author', 'meta[name="author"]', 'content'),
            ('og:title', 'meta[property="og:title"]', 'content'),
            ('og:description', 'meta[property="og:description"]', 'content'),
            ('og:image', 'meta[property="og:image"]', 'content'),
        ]
        
        for key, selector, attr in meta_tags:
            element = soup.select_one(selector)
            if element and element.get(attr):
                metadata[key] = element[attr]
        
        return metadata