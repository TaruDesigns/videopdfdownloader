from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root_redirect():
    return RedirectResponse("/videodownloader")


@router.get("/videodownloader")
async def video_downloader(request: Request):
    """Main Video downloader endpoint, "home" """
    return templates.TemplateResponse(request=request, name="videodownloader.html")
    ...
