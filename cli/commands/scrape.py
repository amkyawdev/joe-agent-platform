"""Scrape command - Extract specific content from web pages."""

import json
import click

from crawler.extractor import ContentExtractor
from crawler.fetcher import WebFetcher


@click.command()
@click.argument('url')
@click.option('--selector', '-s', help='CSS selector for content extraction')
@click.option('--query', '-q', help='Natural language query for content')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'html']), default='text')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def scrape(url: str, selector: str, query: str, format: str, output: str) -> None:
    """Scrape specific content from a URL."""
    fetcher = WebFetcher()
    extractor = ContentExtractor()
    
    html_content = fetcher.fetch(url)
    
    if selector:
        content = extractor.extract_by_selector(html_content, selector)
    elif query:
        content = extractor.extract_by_query(html_content, query)
    else:
        content = extractor.extract_all_text(html_content)
    
    if format == 'json':
        content = json.dumps({'url': url, 'content': content}, indent=2)
    
    if output:
        Path(output).write_text(content)
        click.echo(f"Content saved to {output}")
    else:
        click.echo(content)


from pathlib import Path


def main() -> None:
    scrape()


if __name__ == '__main__':
    scrape()