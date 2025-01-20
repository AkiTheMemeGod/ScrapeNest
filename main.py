import requests

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)


@app.post("/scrape")
def scrape(url: str):

    response = requests.get(url)
    return response.text
