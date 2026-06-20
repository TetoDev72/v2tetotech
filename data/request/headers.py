import random
from data.request.useragents import get_ua
from data.config import MOBILE_IP_PREFIXES, V2PLUS_PRIVACY_HWID


def generate_real_ip() -> str:
    prefix = random.choice(MOBILE_IP_PREFIXES)
    return f"{prefix}.{random.randint(1, 254)}"


def get_spoof_headers(
    hwid: str = None,
    client: str = "happ",
    url: str = None,
    final_url: str = None,
    **kwargs
) -> dict:
    client_lower = client.lower().strip()
    os_name = kwargs.get("os", "Android")

    if client_lower.startswith("v2plus") or client_lower.startswith("yaenot"):
        hwid = V2PLUS_PRIVACY_HWID
    elif not hwid or hwid.lower() in ("random", "default", "none"):
        if client_lower == "happ":
            hwid = "0000000000000000"
        else:
            from helpers.tools.hwid_gen import generate_hwid_from_url
            hwid = generate_hwid_from_url(final_url or url or "")

    ua = get_ua(client_lower, os_name=os_name)

    realip = kwargs.get("realip", None)
    if not realip or realip.lower() in ("random", "default", "none"):
        realip = generate_real_ip()

    forwardedfor = kwargs.get("forwardedfor", None)
    if not forwardedfor or forwardedfor.lower() in ("random", "default", "none"):
        forwardedfor = realip

    return {
        "User-Agent": ua,
        "X-Device-Os": os_name,
        "X-Device-Model": kwargs.get("model", "ELP-NX1"),
        "X-Ver-Os": kwargs.get("osver", "15"),
        "X-Hwid": hwid,
        "X-Real-Ip": realip,
        "X-Forwarded-For": forwardedfor,
    }
