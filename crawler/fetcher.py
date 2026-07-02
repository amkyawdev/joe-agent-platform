"""Fetcher - Web content fetching utilities."""

from typing import Optional, Dict, Any
import httpx
from urllib.parse import urljoin, urlparse


class WebFetcher:
    """Fetch web content via HTTP and browser."""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
    
    def fetch(self, url: str, browser: Optional[Any] = None) -> str:
        """Fetch content from URL."""
        if browser:
            return self._fetch_with_browser(url, browser)
        return self._fetch_with_httpx(url)
    
    def _fetch_with_httpx(self, url: str) -> str:
        """Fetch using httpx."""
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.text
        except httpx.HTTPError as e:
            return f"Error fetching {url}: {str(e)}"
    
    def _fetch_with_browser(self, url: str, browser: Any) -> str:
        """Fetch using browser automation."""
        from crawler.browser import BrowserController
        
        page = browser.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=self.timeout * 1000)
            return page.content()
        except Exception as e:
            return f"Error fetching {url}: {str(e)}"
        finally:
            page.close()
    
    def fetch_many(self, urls: list[str]) -> Dict[str, str]:
        """Fetch multiple URLs concurrently."""
        results = {}
        for url in urls:
            results[url] = self.fetch(url)
        return results
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def normalize_url(self, url: str, base: Optional[str] = None) -> str:
        """Normalize URL relative to base."""
        if base:
            return urljoin(base, url)
        
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"