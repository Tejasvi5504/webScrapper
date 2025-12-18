import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

from app.scrapper.parser import parse_sections

def static_scrape(url: str):
    res = httpx.get(url, timeout=15)
    soup = BeautifulSoup(res.text, "lxml")

    title = soup.title.text.strip() if soup.title else ""
    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        description = desc_tag.get("content", "")

    lang = soup.html.get("lang") if soup.html else "en"
    canonical_tag = soup.find("link", rel="canonical")
    canonical = canonical_tag["href"] if canonical_tag else None

    sections = parse_sections(soup, url)

    return {
        "url": url,
        "scrapedAt": datetime.utcnow().isoformat() + "Z",
        "meta": {
            "title": title,
            "description": description,
            "language": lang,
            "canonical": canonical
        },
        "sections": sections,
        "interactions": {
            "clicks": [],
            "scrolls": 0,
            "pages": [url]
        },
        "errors": []
    }
