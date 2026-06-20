from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse
from helpers.request.request import plain_get
from helpers.tools.link_resolver import resolve_link
from helpers.tools.rebrander import rebrand
import base64

router = APIRouter()

@router.get("/b")
@router.get("/batch")
async def batch(urls: str = Query(...)):
    links = [u.strip() for u in urls.split(",") if u.strip()]
    results = []
    for url in links:
        try:
            final_url = await resolve_link(url)
            res = await plain_get(final_url)
            try:
                padded = res.strip() + '=' * (-len(res.strip()) % 4)
                decoded = base64.b64decode(padded).decode('utf-8')
                results.append(decoded)
            except Exception:
                results.append(res)
        except Exception:
            pass
            
    combined = "\n".join(results)
    branded = rebrand(combined, brand=None, mode="batch") # DEFAULT_BRAND
    return PlainTextResponse(base64.b64encode(branded.encode()).decode())
