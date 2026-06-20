from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from data.config import CHARITY_BATCH_LINKS, CHARITY_BRAND
from helpers.request.request import plain_get
from helpers.tools.rebrander import rebrand
import base64

router = APIRouter()

@router.get("/c")
@router.get("/charity")
@router.get("/z")
async def charity():
    results = []
    for url in CHARITY_BATCH_LINKS:
        try:
            res = await plain_get(url)
            try:
                padded = res.strip() + '=' * (-len(res.strip()) % 4)
                decoded = base64.b64decode(padded).decode('utf-8')
                results.append(decoded)
            except Exception:
                results.append(res)
        except Exception:
            pass
    combined = "\n".join(results)
    branded = rebrand(combined, brand=CHARITY_BRAND, mode=None)
    return PlainTextResponse(base64.b64encode(branded.encode()).decode())
