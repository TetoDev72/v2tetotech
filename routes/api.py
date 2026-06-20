from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import base64
import urllib.parse
from datetime import datetime
from data.config import (
    API_VERSION, PROJECT_NAME, FLAVOR, MIRRORS,
    CHARITY_BATCH_LINKS, DEFAULT_BRAND, CHARITY_BRAND
)
from helpers.tools.link_resolver import resolve_link
from helpers.tools.hwid_gen import generate_hwid_from_url
from helpers.tools.payload_builder import generate_v2tetotech_link
from helpers.tools.rebrander import rebrand
from helpers.tools.payloaddata_parser import parse_payload
from helpers.crypt import happcrypt, happcrypt5
from helpers.request.spoofedrequest import fetch_with_spoof
from helpers.request.request import plain_get
from helpers.parser.parse2il import parse_to_il
from helpers.parser.schemes import clash, sing_box, xray_core

router = APIRouter()

class APIRequest(BaseModel):
    cmd: str
    role: str = "REQUEST"
    data: Optional[dict] = {}

class APIResponse(BaseModel):
    cmd: str
    role: str = "RESPONSE"
    data: dict

ZEROED_VLESS_TEMPLATE = (
    "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443"
    "?encryption=none&flow=xtls-rprx-vision&security=reality"
    "&sni=://microsoft.com&fp=chrome&pbk=dummy_public_key_here&sid=00000000"
)

def _zeroed_key(label: str, value: str) -> str:
    return f"{ZEROED_VLESS_TEMPLATE}#{urllib.parse.quote(label)}: {value}"

async def handle_command(cmd: str, data: dict, request: Request) -> dict:
    cmd = cmd.upper()

    if cmd == "PING":
        return {
            "pong": "hello!",
            "timestamp": datetime.now().isoformat(),
            "version": API_VERSION
        }

    elif cmd == "SERVER_INFO":
        return {
            "name": PROJECT_NAME,
            "version": API_VERSION,
            "flavor": FLAVOR,
            "mirrors": MIRRORS,
            "endpoints": [
                "/s/{link}", "/auto/{link}", "/fetch/{link}",
                "/advsync", "/batch", "/decrypt",
                "/deeplink", "/charity", "/svinfo",
                "/payloadgen", "/spoofdata", "/api"
            ],
            "status": "online"
        }

    elif cmd == "HWID":
        url = data.get("url", "")
        if not url:
            raise HTTPException(400, "Missing 'url' in data")
        return {
            "hwid": generate_hwid_from_url(url),
            "url": url,
            "algorithm": "CRC-16/ARC"
        }

    elif cmd == "DECRYPT":
        link = data.get("link", "")
        if not link:
            raise HTTPException(400, "Missing 'link' in data")
        try:
            if "crypt5/" in link:
                res = await happcrypt5.decrypt(link)
            else:
                res = await happcrypt.decrypt(link)
            return {"status": "success", "url": res}
        except Exception as e:
            raise HTTPException(400, f"Decryption failed: {str(e)}")

    elif cmd == "HEADERS":
        headers = dict(request.headers)
        keys = [
            _zeroed_key("User-Agent", headers.get("user-agent", "unknown")),
            _zeroed_key("RealIP", headers.get("x-real-ip", request.client.host)),
            _zeroed_key("ForwardedFor", headers.get("x-forwarded-for", request.client.host)),
            _zeroed_key("Hwid", headers.get("x-hwid", "0000000000000000")),
            _zeroed_key("Device-Model", headers.get("x-device-model", "unknown")),
            _zeroed_key("Device-Os", headers.get("x-device-os", "unknown")),
            _zeroed_key("Ver-Os", headers.get("x-ver-os", "unknown")),
        ]
        return {
            "client_ip": request.client.host,
            "keys": keys,
            "raw_headers": headers
        }

    elif cmd == "DEVICE":
        ua = request.headers.get("user-agent", "unknown")
        realip = request.headers.get("x-real-ip", request.client.host)
        forwardedfor = request.headers.get("x-forwarded-for", request.client.host)
        hwid = request.headers.get("x-hwid", "0000000000000000")
        model = request.headers.get("x-device-model", "unknown")
        os_name = request.headers.get("x-device-os", "unknown")
        osver = request.headers.get("x-ver-os", "unknown")
        return {
            "keys": [
                _zeroed_key("User-Agent", ua),
                _zeroed_key("RealIP", realip),
                _zeroed_key("ForwardedFor", forwardedfor),
                _zeroed_key("Hwid", hwid),
                _zeroed_key("Device-Model", model),
                _zeroed_key("Device-Os", os_name),
                _zeroed_key("Ver-Os", osver),
            ]
        }

    elif cmd == "DEEPLINK":
        url = data.get("url", "")
        client = data.get("client", "v2rayng")
        mode = data.get("mode", "sync")
        base_url = data.get("base_url", "http://localhost:8000")
        if not url:
            raise HTTPException(400, "Missing 'url' in data")

        try:
            final_url = await resolve_link(url)
        except Exception:
            final_url = url

        if mode == "fetch":
            sub_url = f"{base_url}/f/{urllib.parse.quote(final_url, safe='')}"
        elif mode == "advsync":
            sub_url = f"{base_url}/advsync?p={base64.urlsafe_b64encode(f'link={final_url}'.encode()).decode()}"
        else:  # sync (default)
            sub_url = f"{base_url}/s/{base64.urlsafe_b64encode(final_url.encode()).decode()}"

        schemes = {
            "clash": f"clash://install-config?url={sub_url}",
            "cmfa": f"cmfa://install-config?url={sub_url}",
            "singbox": f"singbox://import-remote-profile?url={sub_url}",
            "v2rayng": f"v2rayng://install-sub?url={sub_url}",
            "v2rayn": f"v2rayn://install-sub?url={sub_url}",
            "nekobox": f"nekobox://install-sub?url={sub_url}",
            "shadowrocket": f"shadowrocket://add/sub://{base64.b64encode(sub_url.encode()).decode()}",
            "stash": f"stash://install-config?url={sub_url}",
            "stash-v2": f"stash-v2://install-config?url={sub_url}",
            "hiddify": f"hiddify://import/{sub_url}",
        }
        return {
            "client": client,
            "mode": mode,
            "subscription_url": sub_url,
            "deeplink": schemes.get(client.lower(), schemes["v2rayng"]),
            "all_deeplinks": schemes
        }

    elif cmd == "CHARITY":
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
        return {
            "subscription": base64.b64encode(branded.encode()).decode(),
            "brand": CHARITY_BRAND
        }

    elif cmd == "BATCH":
        urls_str = data.get("urls", "")
        urls = [u.strip() for u in urls_str.split(",") if u.strip()]
        if not urls:
            raise HTTPException(400, "Missing 'urls' in data (comma-separated)")

        results = []
        for url in urls:
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
        return {
            "subscription": base64.b64encode(combined.encode()).decode(),
            "count": len(results)
        }

    elif cmd == "SYNC":
        url = data.get("url", "")
        if not url:
            raise HTTPException(400, "Missing 'url' in data")
        try:
            final_url = await resolve_link(url)
        except Exception as e:
            raise HTTPException(400, f"Link resolution failed: {str(e)}")

        hwid = data.get("hwid", "default")
        if hwid.lower() in ("default", "crc16", "sticky"):
            hwid = generate_hwid_from_url(final_url)

        client = data.get("client", "happ")
        content = await fetch_with_spoof(
            final_url, hwid=hwid, client=client, final_url=final_url
        )

        content = rebrand(content, brand=None, mode=None)
        return {"subscription": content}

    elif cmd == "FETCH":
        url = data.get("url", "")
        if not url:
            raise HTTPException(400, "Missing 'url' in data")
        try:
            final_url = await resolve_link(url)
        except Exception as e:
            raise HTTPException(400, f"Link resolution failed: {str(e)}")

        client = data.get("client", "auto")
        raw = await plain_get(final_url)
        il = parse_to_il(raw, client_ua=client, target_url=final_url)

        if "clash" in client.lower() or "mihomo" in client.lower():
            return {"format": "clash", "content": clash.to_clash_yaml(il)}
        elif "sing-box" in client.lower() or "sfa" in client.lower():
            return {"format": "sing-box", "content": sing_box.to_singbox_json(il)}
        else:
            return {"format": "xray", "content": xray_core.to_xray_base64(il)}

    elif cmd in ("ADVANCED_SYNC", "CUSTOM_SYNC"):
        link = data.get("link", "")
        if not link:
            raise HTTPException(400, "Missing 'link' in data")
        try:
            final_url = await resolve_link(link)
        except Exception as e:
            raise HTTPException(400, f"Link resolution failed: {str(e)}")

        hwid = data.get("hwid", "default")
        if hwid.lower() in ("default", "crc16", "sticky"):
            hwid = generate_hwid_from_url(final_url)

        ua = data.get("ua", "happ")
        fmt = data.get("format", "auto")
        raw = await fetch_with_spoof(
            final_url, hwid=hwid, client=ua, final_url=final_url,
            os=data.get("os", "Android"),
            model=data.get("model", "ELP-NX1"),
            osver=data.get("osver", "15")
        )

        brand_keys = ["title", "updateint", "webpage", "lastupd", "announce"]
        brand = {k: data.get(k) for k in brand_keys if data.get(k)}
        raw = rebrand(raw, brand if brand else None, mode="advsync" if brand else None)

        il = parse_to_il(raw, client_ua=ua, target_url=final_url)
        if fmt == "clash":
            return {"format": "clash", "content": clash.to_clash_yaml(il)}
        elif fmt == "sing-box":
            return {"format": "sing-box", "content": sing_box.to_singbox_json(il)}
        elif fmt in ("xray", "v2ray"):
            return {"format": "xray", "content": xray_core.to_xray_base64(il)}
        else:
            return {"format": "raw", "content": raw}

    elif cmd == "PAYLOAD_GEN":
        link = data.get("link", "")
        if not link:
            raise HTTPException(400, "Missing 'link' in data")
        try:
            final_url = await resolve_link(link)
        except Exception:
            final_url = link

        strategy = data.get("strategy", "best")
        mode = data.get("mode", "sync")
        base_url = data.get("base_url", "http://localhost:8000")
        result = generate_v2tetotech_link(base_url, final_url, strategy)
        result["mode"] = mode
        return result

    elif cmd == "WHITELIST_BYPASS_LINK":
        from helpers.tools.wlbypasslinks import apply_bypass, list_strategies

        url = data.get("url", "")
        strategy = data.get("strategy", "yandex_translate")

        if not url:
            raise HTTPException(400, "Missing 'url' in data")

        try:
            final_url = await resolve_link(url)
        except Exception:
            final_url = url

        result = apply_bypass(final_url, strategy)
        if not result["success"]:
            raise HTTPException(400, result["error"])

        result["available_strategies"] = list_strategies()
        return result

    else:
        raise HTTPException(400, f"Unknown command: {cmd}")

@router.post("/api")
@router.post("/a")
async def api_endpoint(req: APIRequest, request: Request):
    """
    Формат запроса:
    {
        "cmd": "COMMAND_NAME",
        "role": "REQUEST",
        "data": { ... }
    }

    Формат ответа:
    {
        "cmd": "COMMAND_NAME",
        "role": "RESPONSE",
        "data": { ... }
    }
    """
    try:
        result = await handle_command(req.cmd, req.data or {}, request)
        return APIResponse(cmd=req.cmd, role="RESPONSE", data=result)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Command execution failed: {str(e)}")
