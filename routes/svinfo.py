from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from data.config import API_VERSION, PROJECT_NAME, FLAVOR, MIRRORS, REPO_URL

router = APIRouter()

@router.get("/v")
@router.get("/svinfo")
async def server_info():
    mirrors_text = "\n".join([f"mirror: {m}" for m in MIRRORS]) if MIRRORS else "mirror: none"
    text = f"""{PROJECT_NAME}
version: {API_VERSION}
repo: {REPO_URL}
{mirrors_text}
status: online"""
    return PlainTextResponse(content=text, media_type="text/plain; charset=utf-8")
