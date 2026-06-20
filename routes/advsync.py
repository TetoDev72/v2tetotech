from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse, Response
from helpers.request.spoofedrequest import fetch_with_spoof
from helpers.tools.payloaddata_parser import parse_payload
from helpers.parser.parse2il import parse_to_il
from helpers.parser.schemes import clash, sing_box, xray_core
from helpers.tools.rebrander import rebrand
from helpers.tools.link_resolver import resolve_link
from helpers.tools.hwid_gen import generate_hwid_from_url
import base64

router = APIRouter()

@router.get("/x")
@router.get("/advsync")
async def advsync(p: str = Query(None), request: Request = None):
    params = {}
    if p:
        try:
            padded = p + '=' * (-len(p) % 4)
            json_str = base64.urlsafe_b64decode(padded).decode('utf-8')
            params = parse_payload(json_str)
        except Exception as e:
            raise HTTPException(400, f"Invalid payload: {e}")

    link = params.get("link")
    if not link:
        raise HTTPException(400, "Missing 'link' in payload")

    try:
        final_url = await resolve_link(link)
    except Exception as e:
        raise HTTPException(400, f"Link resolution failed: {str(e)}")

    hwid = params.get("hwid", "default")
    if not hwid or hwid.lower() in ("default", "none", "crc16", "sticky"):
        hwid = generate_hwid_from_url(final_url)

    raw = await fetch_with_spoof(
        final_url,
        hwid=hwid,
        client=params.get("ua", "happ"),
        final_url=final_url,
        os=params.get("os", "Android"),
        model=params.get("model", "ELP-NX1"),
        osver=params.get("osver", "15")
    )

    brand_keys = ["title", "updateint", "webpage", "lastupd", "announce"]
    brand = {k: params.get(k) for k in brand_keys if params.get(k)}

    raw = rebrand(raw, brand if brand else None, mode="advsync" if brand else None)

    fmt = params.get("format", "auto").lower()
    ua = request.headers.get("user-agent", "").lower() if request else ""

    il = parse_to_il(raw, client_ua=ua, target_url=final_url)

    if fmt == "clash" or ("clash" in ua and fmt == "auto"):
        return Response(content=clash.to_clash_yaml(il), media_type="text/yaml")
    elif fmt == "sing-box" or ("sing-box" in ua and fmt == "auto"):
        return Response(content=sing_box.to_singbox_json(il), media_type="application/json")
    elif fmt in ("xray", "v2ray"):
        return PlainTextResponse(xray_core.to_xray_base64(il))

    return PlainTextResponse(raw)
