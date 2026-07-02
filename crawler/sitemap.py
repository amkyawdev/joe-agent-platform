"""Sitemap - Sitemap parsing utilities."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import httpx
from urllib.parse import urljoin


@dataclass
class SitemapURL:
    loc: str
    lastmod: Optional[str] = None
    changefreq: Optional[str] = None
    priority: Optional[float] = None


class SitemapParser:
    """Parse XML sitemaps."""
    
    def __init__(self):
        self.urls: List[SitemapURL] = []
    
    def parse(self, xml_content: str) -> List[SitemapURL]:
        """Parse sitemap XML."""
        self.urls = []
        
        try:
            root = ET.fromstring(xml_content)
            namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            for url in root.findall('.//ns:url', namespaces):
                loc = url.find('ns:loc', namespaces)
                lastmod = url.find('ns:lastmod', namespaces)
                changefreq = url.find('ns:changefreq', namespaces)
                priority = url.find('ns:priority', namespaces)
                
                self.urls.append(SitemapURL(
                    loc=loc.text if loc is not None else "",
                    lastmod=lastmod.text if lastmod is not None else None,
                    changefreq=changefreq.text if changefreq is not None else None,
                    priority=float(priority.text) if priority is not None else None
                ))
        
        except ET.ParseError:
            pass
        
        return self.urls
    
    def fetch(self, url: str) -> List[SitemapURL]:
        """Fetch and parse sitemap from URL."""
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url)
                response.raise_for_status()
                return self.parse(response.text)
        except Exception:
            return []
    
    def discover_sitemap(self, base_url: str) -> Optional[str]:
        """Discover sitemap URL for a website."""
        common_paths = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/wp-sitemap.xml',
            '/sitemap/index.xml'
        ]
        
        for path in common_paths:
            sitemap_url = urljoin(base_url, path)
            try:
                with httpx.Client(timeout=10.0) as client:
                    response = client.head(sitemap_url)
                    if response.status_code == 200:
                        return sitemap_url
            except Exception:
                continue
        
        return None


class SitemapCrawler:
    """Crawl URLs from sitemaps."""
    
    def __init__(self):
        self.parser = SitemapParser()
    
    def get_urls(self, sitemap_url: str, max_urls: int = 1000) -> List[str]:
        """Get URLs from sitemap."""
        urls = self.parser.fetch(sitemap_url)
        return [url.loc for url in urls[:max_urls]]
    
    def filter_by_pattern(self, urls: List[str], pattern: str) -> List[str]:
        """Filter URLs by regex pattern."""
        import re
        regex = re.compile(pattern)
        return [url for url in urls if regex.search(url)]