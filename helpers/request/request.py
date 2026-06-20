import httpx
from data.config import REQUEST_TIMEOUT

async def plain_get(url: str) -> str:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, follow_redirects=True) as c:
        return (await c.get(url)).text
