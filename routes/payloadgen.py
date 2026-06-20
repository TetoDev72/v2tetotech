from fastapi import APIRouter, Query
from helpers.tools.payload_builder import generate_v2tetotech_link
from helpers.tools.link_resolver import resolve_link

router = APIRouter()

@router.get("/pg")
@router.get("/payloadgen")
@router.get("/y")
async def payloadgen(
    link: str = Query(...),
    strategy: str = Query("best"),
    base_url: str = Query("http://localhost:8000")
):
    try:
        final_url = await resolve_link(link)
    except Exception:
        final_url = link
    
    return generate_v2tetotech_link(base_url, final_url, strategy)
