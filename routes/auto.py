from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from helpers.request.spoofedrequest import fetch_with_spoof
from helpers.tools.link_resolver import resolve_link
from helpers.tools.rebrander import rebrand

router = APIRouter()

@router.get("/i/{sub_url:path}")
@router.get("/auto/{sub_url:path}")
async def auto_sync(sub_url: str):
    final_url = await resolve_link(sub_url)
    content = await fetch_with_spoof(final_url, hwid="default", final_url=final_url)
    content = rebrand(content, brand=None, mode="auto") # DEFAULT_BRAND
    return PlainTextResponse(content)
