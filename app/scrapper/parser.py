from urllib.parse import urljoin

def parse_sections(soup, base_url):
    sections = []
    section_tags = soup.find_all(["section", "main", "article", "nav", "footer"])

    for idx, tag in enumerate(section_tags):
        text = tag.get_text(" ", strip=True)
        if not text:
            continue

        headings = [h.get_text(strip=True) for h in tag.find_all(["h1", "h2", "h3"])]
        label = headings[0] if headings else " ".join(text.split()[:6])

        links = []
        for a in tag.find_all("a", href=True):
            links.append({
                "text": a.get_text(strip=True),
                "href": urljoin(base_url, a["href"])
            })

        images = []
        for img in tag.find_all("img"):
            images.append({
                "src": urljoin(base_url, img.get("src", "")),
                "alt": img.get("alt", "")
            })

        raw_html = str(tag)[:1000]

        sections.append({
            "id": f"section-{idx}",
            "type": "section",
            "label": label,
            "sourceUrl": base_url,
            "content": {
                "headings": headings,
                "text": text,
                "links": links,
                "images": images,
                "lists": [],
                "tables": []
            },
            "rawHtml": raw_html,
            "truncated": len(str(tag)) > 1000
        })

    return sections
