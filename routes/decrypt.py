from fastapi import APIRouter, Query, HTTPException
from helpers.tools.link_resolver import resolve_link

router = APIRouter()

@router.get("/e")
@router.get("/decrypt")
async def decrypt_link(link: str = Query(...)):
    try:
        final_url = await resolve_link(link)
        return {"status": "success", "url": final_url}
    except Exception as e:
        raise HTTPException(400, f"Decryption failed: {str(e)}")
