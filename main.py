from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
import httpx
from fastapi.templating import Jinja2Templates
app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)


@app.get("/scrape", response_class=HTMLResponse)
async def scrape(url: str = Query(..., description="The URL to scrape")):
    try:
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("URL must start with 'http://' or 'https://'")

        # Fetch the content
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        return HTMLResponse(content=response.text)

    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=f"Request error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
