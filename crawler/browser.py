"""Browser - Browser automation for web crawling."""

from typing import Optional, Dict, Any, TYPE_CHECKING
from contextlib import contextmanager
import asyncio

if TYPE_CHECKING:
    from playwright.sync_api import sync_playwright, Browser, Page


class BrowserPool:
    """Manages a pool of browser instances."""
    
    def __init__(self, headless: bool = True, num_browsers: int = 2):
        self.headless = headless
        self.num_browsers = num_browsers
        self._playwright = None
        self._browsers = []
    
    def start(self) -> None:
        """Initialize browser pool."""
        from playwright.sync_api import sync_playwright
        self._playwright = sync_playwright().start()
        for _ in range(self.num_browsers):
            browser = self._playwright.chromium.launch(headless=self.headless)
            self._browsers.append(browser)
    
    def stop(self) -> None:
        """Close all browsers."""
        for browser in self._browsers:
            browser.close()
        if self._playwright:
            self._playwright.stop()
        self._browsers = []
    
    @contextmanager
    def get_browser(self):
        """Get a browser from the pool."""
        if not self._browsers:
            self.start()
        
        browser = self._browsers[0]
        try:
            yield browser
        finally:
            pass
    
    def close(self) -> None:
        """Close the browser pool."""
        self.stop()


class BrowserController:
    """Control browser interactions."""
    
    def __init__(self, browser):
        self.browser = browser
    
    def new_page(self):
        """Create a new page."""
        return self.browser.new_page()
    
    def navigate(self, page, url: str, wait_until: str = "networkidle") -> None:
        """Navigate to a URL."""
        page.goto(url, wait_until=wait_until)
    
    def screenshot(self, page, path: str) -> None:
        """Take a screenshot."""
        page.screenshot(path=path)
    
    def get_html(self, page) -> str:
        """Get page HTML."""
        return page.content()
    
    def click(self, page, selector: str) -> None:
        """Click an element."""
        page.click(selector)
    
    def type_text(self, page, selector: str, text: str) -> None:
        """Type text into an element."""
        page.fill(selector, text)
    
    def wait_for_selector(self, page, selector: str, timeout: int = 30000) -> None:
        """Wait for selector."""
        page.wait_for_selector(selector, timeout=timeout)


class AsyncBrowserPool:
    """Async browser pool for concurrent operations."""
    
    def __init__(self, headless: bool = True, num_browsers: int = 2):
        self.headless = headless
        self.num_browsers = num_browsers
        self._playwright = None
        self._browsers: list = []
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
    
    async def start(self) -> None:
        """Initialize async browser pool."""
        from playwright.async_api import async_playwright
        self._playwright = await async_playwright().start()
        for _ in range(self.num_browsers):
            browser = await self._playwright.chromium.launch(headless=self.headless)
            self._browsers.append(browser)
    
    async def stop(self) -> None:
        """Close all browsers."""
        for browser in self._browsers:
            await browser.close()
        if self._playwright:
            await self._playwright.stop()
        self._browsers = []
    
    @property
    def browsers(self) -> list:
        return self._browsers