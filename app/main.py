import asyncio
import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from datetime import datetime

from app.scrapper.static import static_scrape
from app.scrapper.js import js_scrape

# Fix for Windows asyncio and Playwright (Proactor lacks subprocess support)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


class ScrapeRequest(BaseModel):
    url: HttpUrl


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/scrape")
async def scrape(req: ScrapeRequest):
    url = str(req.url)
    errors = []

    try:
        result = static_scrape(url)
        if len(result["sections"]) < 1 or len(result["sections"][0]["content"]["text"]) < 50:
            raise Exception("Static content insufficient")
        strategy = "static"
    except Exception as e:
        errors.append({"message": str(e), "phase": "static"})
        result = await js_scrape(url)
        strategy = "js"

    result["strategy"] = strategy
    result["errors"].extend(errors)

    return {"result": result}
