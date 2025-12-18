# Design Notes

## Static vs JS Fallback
Static scraping is attempted first. If insufficient text is found, Playwright JS rendering is used.

## Wait Strategy for JS
- Network idle
- Scroll-based loading

## Click & Scroll Strategy
- Infinite scroll (3 scrolls)
- No pagination or tab clicks

## Section Grouping & Labels
Sections are grouped by semantic HTML tags. Labels are derived from headings or first 5–6 words.

## Noise Filtering & Truncation
No advanced filtering. rawHtml truncated at 1000 characters.
