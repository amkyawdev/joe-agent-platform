"""Robots - robots.txt parsing and compliance."""

from typing import List, Set, Optional
from urllib.parse import urlparse
import httpx


class RobotsParser:
    """Parse and respect robots.txt files."""
    
    def __init__(self):
        self.rules: dict[str, dict] = {}
    
    def fetch(self, url: str, user_agent: str = "*") -> bool:
        """Fetch and parse robots.txt for a URL."""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(robots_url)
                if response.status_code == 200:
                    self._parse_rules(response.text)
                    return True
        except Exception:
            pass
        
        return False
    
    def _parse_rules(self, content: str) -> None:
        """Parse robots.txt content."""
        current_agent = None
        
        for line in content.splitlines():
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue
            
            if line.lower().startswith('user-agent:'):
                current_agent = line.split(':', 1)[1].strip()
                if current_agent not in self.rules:
                    self.rules[current_agent] = {'allow': [], 'disallow': []}
            
            elif line.lower().startswith('allow:'):
                if current_agent:
                    path = line.split(':', 1)[1].strip()
                    self.rules[current_agent]['allow'].append(path)
            
            elif line.lower().startswith('disallow:'):
                if current_agent:
                    path = line.split(':', 1)[1].strip()
                    self.rules[current_agent]['disallow'].append(path)
    
    def can_fetch(self, url: str, user_agent: str = "*") -> bool:
        """Check if URL can be fetched."""
        parsed = urlparse(url)
        path = parsed.path or '/'
        
        if 'user-agent' in self.rules:
            return self._check_path(path, self.rules.get(user_agent, self.rules.get('*', {'allow': [], 'disallow': []})))
        
        return True
    
    def _check_path(self, path: str, rules: dict) -> bool:
        """Check if path is allowed."""
        for disallow in rules.get('disallow', []):
            if path.startswith(disallow):
                for allow in rules.get('allow', []):
                    if path.startswith(allow):
                        return True
                return False
        
        return True
    
    def get_crawl_delay(self, user_agent: str = "*") -> Optional[float]:
        """Get crawl delay for user agent."""
        return None