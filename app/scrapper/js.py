import asyncio
import sys

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime

from app.scrapper.parser import parse_sections


async def _js_scrape(url: str):
    interactions = {"clicks": [], "scrolls": 0, "pages": [url]}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle")

        # Scroll 3 times to load lazy content
        for _ in range(3):
            await page.mouse.wheel(0, 2000)
            await page.wait_for_timeout(1500)
            interactions["scrolls"] += 1

        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "lxml")
    sections = parse_sections(soup, url)

    return {
        "url": url,
        "scrapedAt": datetime.utcnow().isoformat() + "Z",
        "meta": {
            "title": soup.title.text if soup.title else "",
            "description": "",
            "language": "en",
            "canonical": None
        },
        "sections": sections,
        "interactions": interactions,
        "errors": []
    }


def _run_js_scrape_in_new_loop(url: str):
    """Run Playwright in a fresh selector loop so subprocesses work on Windows."""
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.run(_js_scrape(url))


async def js_scrape(url: str):
    loop = asyncio.get_running_loop()

    # On Windows, Proactor loops can't spawn subprocesses (Playwright needs them).
    if sys.platform == "win32" and isinstance(loop, asyncio.ProactorEventLoop):
        return await asyncio.to_thread(_run_js_scrape_in_new_loop, url)

    return await _js_scrape(url)
