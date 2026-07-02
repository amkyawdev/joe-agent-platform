"""Crawl command - Web crawling with browser automation."""

import click
from pathlib import Path

from crawler.browser import BrowserPool
from crawler.fetcher import WebFetcher
from crawler.parser import HTMLParser
from crawler.cleaner import ContentCleaner


@click.command()
@click.argument('url')
@click.option('--depth', '-d', type=int, default=1, help='Crawl depth')
@click.option('--output', '-o', type=click.Path(), default='output.html', help='Output file')
@click.option('--markdown/--html', default=False, help='Convert to markdown')
@click.option('--headless/--no-headless', default=True, help='Run browser in headless mode')
def crawl(url: str, depth: int, output: str, markdown: bool, headless: bool) -> None:
    """Crawl a website and extract content."""
    browser_pool = BrowserPool(headless=headless)
    fetcher = WebFetcher()
    parser = HTMLParser()
    cleaner = ContentCleaner()
    
    try:
        with browser_pool.get_browser() as browser:
            click.echo(f"Crawling {url} (depth={depth})...")
            
            html_content = fetcher.fetch(url, browser)
            parsed = parser.parse(html_content, url)
            cleaned = cleaner.clean(parsed)
            
            if markdown:
                from crawler.markdown import to_markdown
                content = to_markdown(cleaned)
            else:
                content = cleaned
            
            Path(output).write_text(content)
            click.echo(f"Content saved to {output}")
            
    finally:
        browser_pool.close()


def main() -> None:
    crawl()


if __name__ == '__main__':
    crawl()