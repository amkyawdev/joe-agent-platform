"""Markdown - Convert content to Markdown format."""

from typing import Any
from bs4 import BeautifulSoup
import markdownify


class MarkdownConverter:
    """Convert HTML to Markdown."""
    
    def __init__(self):
        self.conversion_options = {
            'heading_style': 'ATX',
            'bullets': '-',
            'strip': ['script', 'style', 'nav', 'footer', 'header']
        }
    
    def convert(self, html: str) -> str:
        """Convert HTML to Markdown."""
        soup = BeautifulSoup(html, 'lxml')
        
        for tag in self.conversion_options.get('strip', []):
            for element in soup.find_all(tag):
                element.decompose()
        
        return markdownify.markdownify(
            html,
            heading_style=self.conversion_options['heading_style'],
            bullets=self.conversion_options['bullets']
        )
    
    def convert_element(self, element: Any) -> str:
        """Convert a BeautifulSoup element to Markdown."""
        return markdownify.markdownify(str(element))


def to_markdown(html: str) -> str:
    """Convert HTML to Markdown (convenience function)."""
    converter = MarkdownConverter()
    return converter.convert(html)


def to_markdown_with_images(html: str, base_url: str = "") -> str:
    """Convert HTML to Markdown preserving images."""
    soup = BeautifulSoup(html, 'lxml')
    
    for tag in ['script', 'style', 'nav', 'footer', 'header']:
        for element in soup.find_all(tag):
            element.decompose()
    
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if base_url and not src.startswith(('http://', 'https://')):
            src = base_url + src
        alt = img.get('alt', 'image')
        img.replace_with(soup.new_string(f'![{alt}]({src})'))
    
    return markdownify.markdownify(str(soup))