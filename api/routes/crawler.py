"""Crawler Routes - Web crawling endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from crawler.fetcher import WebFetcher
from crawler.parser import HTMLParser
from crawler.cleaner import ContentCleaner
from crawler.extractor import ContentExtractor


router = APIRouter()


class CrawlRequest(BaseModel):
    url: str
    extract_main_content: bool = True


class CrawlResponse(BaseModel):
    url: str
    title: str
    content: str
    links: list[str] = []
    images: list[str] = []
    metadata: dict = {}


@router.post("/crawler/crawl", response_model=CrawlResponse)
async def crawl_url(request: CrawlRequest) -> CrawlResponse:
    """Crawl a URL and extract content."""
    try:
        fetcher = WebFetcher()
        parser = HTMLParser()
        cleaner = ContentCleaner()
        
        html = fetcher.fetch(request.url)
        parsed = parser.parse(html, request.url)
        
        content = parsed.text
        if request.extract_main_content:
            extractor = ContentExtractor()
            content = extractor.extract_main_content(html)
        
        content = cleaner.clean(content)
        
        return CrawlResponse(
            url=request.url,
            title=parsed.title,
            content=content,
            links=parsed.links,
            images=parsed.images,
            metadata=parsed.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crawler/scrape")
async def scrape_url(url: str, selector: str = None) -> dict:
    """Scrape specific content from URL."""
    try:
        fetcher = WebFetcher()
        extractor = ContentExtractor()
        
        html = fetcher.fetch(url)
        
        if selector:
            content = extractor.extract_by_selector(html, selector)
        else:
            content = extractor.extract_all_text(html)
        
        return {"url": url, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))