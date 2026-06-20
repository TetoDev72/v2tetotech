from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from helpers.request.request import plain_get
from helpers.parser.parse2il import parse_to_il
from helpers.parser.schemes import clash, sing_box, xray_core
from helpers.tools.rebrander import rebrand
from helpers.tools.link_resolver import resolve_link

router = APIRouter()

@router.get("/f/{sub_url:path}")
@router.get("/fetch/{sub_url:path}")
async def fetch_auto(sub_url: str, request: Request):
    final_url = await resolve_link(sub_url)
    raw = await plain_get(final_url)
    raw = rebrand(raw, brand=None, mode="fetch") # DEFAULT_BRAND
    
    ua = request.headers.get("user-agent", "").lower()
    il = parse_to_il(raw, client_ua=ua, target_url=final_url)

    if "clash" in ua or "mihomo" in ua or "cmfa" in ua:
        return Response(content=clash.to_clash_yaml(il), media_type="text/yaml")
    elif "sing-box" in ua or "sfa" in ua or "nekobox" in ua:
        return Response(content=sing_box.to_singbox_json(il), media_type="application/json")
    else:
        return PlainTextResponse(xray_core.to_xray_base64(il))
