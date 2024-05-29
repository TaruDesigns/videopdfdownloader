from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ytdownloader import ytdownloader as ytdl

router = APIRouter()

templates = Jinja2Templates(directory="templates")


class URLRequest(BaseModel):
    url: str


@router.get("/")
async def root_redirect():
    return RedirectResponse("/videodownloader")


@router.post("/ytdownloadsplit")
async def video_downloader(url: URLRequest):
    """Main Video downloader endpoint, "home" """
    outfile, videotitle = ytdl.get_pdf_from_yt_url(url=url.url)
    return FileResponse(
        outfile, filename=f"{videotitle}.pdf", media_type="application/pdf"
    )
    ...
