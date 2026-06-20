from fastapi import APIRouter, Query
import urllib.parse

router = APIRouter()

@router.get("/d")
@router.get("/deeplink")
async def deeplink(
    url: str = Query(...),
    client: str = Query("v2rayng"),
    mode: str = Query("sync"),
    base_url: str = Query("http://localhost:8000")
):
    if mode == "fetch":
        sub_url = f"{base_url}/f/{urllib.parse.quote(url, safe='')}"
    elif mode == "advsync":
        import base64
        p = base64.urlsafe_b64encode(f"link={url}".encode()).decode()
        sub_url = f"{base_url}/advsync?p={p}"
    else:
        import base64
        b64 = base64.urlsafe_b64encode(url.encode()).decode()
        sub_url = f"{base_url}/s/{b64}"
    
    schemes = {
        "clash": f"clash://install-config?url={sub_url}",  # clash-based
        "cmfa": f"cmfa://install-config?url={sub_url}",  # clash meta/mihomo
        "singbox": f"singbox://import-remote-profile?url={sub_url}",  # sfa (sing-box for android)
        "v2rayng": f"v2rayng://install-sub?url={sub_url}",  # v2rayNG
        "v2rayn": f"v2rayn://install-sub?url={sub_url}",  # v2rayN
        "nekobox": f"nekobox://install-sub?url={sub_url}",  # NekoBox
        "shadowrocket": f"shadowrocket://add/sub://{base64.b64encode(sub_url.encode()).decode()}",  # Shadowrocket
        "stash": f"stash://install-config?url={sub_url}",  # Stash
        "hiddify": f"hiddify://import/{sub_url}",  # Hiddify
    }
    
    return {
        "client": client,
        "mode": mode,
        "subscription_url": sub_url,
        "deeplink": schemes.get(client.lower(), schemes["v2rayng"]),
        "all_deeplinks": schemes
    }
