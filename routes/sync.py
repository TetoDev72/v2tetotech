from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse, Response
import hashlib
from helpers.request.spoofedrequest import fetch_with_spoof
from helpers.parser.parse2il import parse_to_il
from helpers.parser.schemes import clash, sing_box, xray_core
from helpers.tools.rebrander import rebrand
from helpers.tools.link_resolver import resolve_link

router = APIRouter()

@router.get("/s/{encoded_link}")
async def smart_sync(encoded_link: str, request: Request):
    try:
        final_url = await resolve_link(encoded_link)
    except Exception as e:
        raise HTTPException(400, f"Link resolution failed: {str(e)}")

    client_ip = request.client.host
    stable_hwid = hashlib.md5(client_ip.encode()).hexdigest()[:16].upper()

    raw_sub = await fetch_with_spoof(final_url, hwid=stable_hwid, final_url=final_url)

    raw_sub = rebrand(raw_sub, brand=None, mode=None)

    ua = request.headers.get("user-agent", "").lower()
    il = parse_to_il(raw_sub, client_ua=ua, target_url=final_url)

    if not il.nodes:
        raise HTTPException(400, "Provider returned stub/fake subscription.")

    if "clash" in ua or "mihomo" in ua:
        return Response(content=clash.to_clash_yaml(il), media_type="text/yaml")
    elif "sing-box" in ua or "nekobox" in ua or "sfa" in ua:
        return Response(content=sing_box.to_singbox_json(il), media_type="application/json")
    else:
        return PlainTextResponse(xray_core.to_xray_base64(il))
