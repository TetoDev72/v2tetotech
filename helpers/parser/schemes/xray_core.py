import base64
from urllib.parse import quote
from helpers.parser.schemes.il import ILSubscription

def to_xray_base64(il: ILSubscription) -> str:
    lines = []
    for n in il.nodes:
        if n.protocol == "vless":
            query_parts = []
            if n.flow: query_parts.append(f"flow={n.flow}")
            query_parts.append(f"type={n.network}")
            query_parts.append(f"security={n.security}")
            if n.sni: query_parts.append(f"sni={n.sni}")
            if n.fp: query_parts.append(f"fp={n.fp}")
            if n.pbk: query_parts.append(f"pbk={n.pbk}")
            if n.sid: query_parts.append(f"sid={n.sid}")
            if n.path: query_parts.append(f"path={quote(n.path)}")
            if n.host: query_parts.append(f"host={n.host}")
            if n.alpn: query_parts.append(f"alpn={','.join(n.alpn)}")
            
            query_str = "?" + "&".join(query_parts) if query_parts else ""
            fragment = "#" + quote(n.name) if n.name else ""
            lines.append(f"vless://{n.uuid}@{n.server}:{n.port}{query_str}{fragment}")
            
        elif n.protocol == "trojan":
            query_parts = []
            if n.sni: query_parts.append(f"sni={n.sni}")
            query_str = "?" + "&".join(query_parts) if query_parts else ""
            fragment = "#" + quote(n.name) if n.name else ""
            lines.append(f"trojan://{n.uuid}@{n.server}:{n.port}{query_str}{fragment}")
            
        elif n.protocol == "ss":
            userinfo = base64.b64encode(f"{n.method}:{n.uuid}".encode()).decode()
            fragment = "#" + quote(n.name) if n.name else ""
            lines.append(f"ss://{userinfo}@{n.server}:{n.port}{fragment}")

    joined_text = "\n".join(lines)
    return base64.b64encode(joined_text.encode('utf-8')).decode('utf-8')
