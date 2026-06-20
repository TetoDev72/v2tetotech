import httpx
import hashlib
import os
import time
from data.request.headers import get_spoof_headers
from data.config import (
    REQUEST_TIMEOUT, CACHE_TTL_SECONDS, CACHE_DIR,
    UA_FRIENDLY_KEYWORDS, SPOOF_FALLBACK_CHAIN,
    CLIENT_UAS, BROWSER_UAS
)
from helpers.tools.hwid_gen import generate_hwid_from_url

os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(url: str, hwid: str) -> str:
    return os.path.join(
        CACHE_DIR,
        hashlib.md5(f"{url}|{hwid}".encode()).hexdigest() + ".cache"
    )


def is_ua_friendly(url: str) -> bool:
    url_lower = url.lower()
    return any(kw in url_lower for kw in UA_FRIENDLY_KEYWORDS)


async def fetch_with_spoof(
    url: str,
    hwid: str = "default",
    client: str = None,
    final_url: str = None,
    **kwargs
) -> str:
    if is_ua_friendly(url):
        from helpers.request.request import plain_get
        return await plain_get(url)

    if not hwid or hwid.lower() in ("random", "default", "none"):
        if client and client.lower() == "happ":
            hwid = "0000000000000000"
        else:
            hwid = generate_hwid_from_url(final_url or url)

    path = _cache_path(url, hwid)
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < CACHE_TTL_SECONDS:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    if client and client.lower() not in ("default", "auto", "chain", "none"):
        clients_to_try = [client.lower()]
    else:
        clients_to_try = SPOOF_FALLBACK_CHAIN

    last_error = None
    last_response = None

    for c_name in clients_to_try:
        from data.request.useragents import get_ua
        os_name = kwargs.get("os", "Android")
        ua = get_ua(c_name, os_name=os_name)

        current_hwid = "0000000000000000" if c_name == "happ" else hwid

        headers = get_spoof_headers(
            hwid=current_hwid,
            client=c_name,
            final_url=final_url or url,
            **kwargs
        )
        headers["User-Agent"] = ua

        try:
            async with httpx.AsyncClient(
                timeout=REQUEST_TIMEOUT, follow_redirects=True
            ) as c:
                resp = await c.get(url, headers=headers)

                if resp.status_code == 200 and len(resp.text.strip()) > 10:
                    last_response = resp.text

                    if ("@0.0.0.0:1" not in resp.text and
                        "limit of devices" not in resp.text.lower()):
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(resp.text)

                    return resp.text

        except Exception as e:
            last_error = e
            continue

    if last_response:
        return last_response
    raise Exception(f"All spoof profiles failed for {url}. Last error: {last_error}")
