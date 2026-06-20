import json
from helpers.parser.schemes.il import ILSubscription

def to_singbox_json(il: ILSubscription) -> str:
    outbounds = []
    
    for n in il.nodes:
        if n.protocol == "vless":
            ob = {
                "tag": n.name or f"vless-{n.server}",
                "type": "vless",
                "server": n.server,
                "server_port": n.port,
                "uuid": n.uuid,
                "packet_encoding": "xudp",
            }
            if n.flow: ob["flow"] = n.flow
            
            if n.security in ("tls", "reality"):
                tls = {
                    "enabled": True, 
                    "server_name": n.sni or n.server,
                    "utls": {"enabled": True, "fingerprint": n.fp or "chrome"}
                }
                if n.security == "reality" and n.pbk:
                    tls["reality"] = {
                        "enabled": True,
                        "public_key": n.pbk,
                        "short_id": n.sid or ""
                    }
                ob["tls"] = tls
                
            outbounds.append(ob)
            
        elif n.protocol == "trojan":
            ob = {
                "tag": n.name or f"trojan-{n.server}",
                "type": "trojan",
                "server": n.server,
                "server_port": n.port,
                "password": n.uuid,
                "tls": {"enabled": True, "server_name": n.sni or n.server}
            }
            outbounds.append(ob)

    config = {
        "log": {"level": "info", "timestamp": True},
        "dns": {
            "servers": [
                {"tag": "google", "address": "https://8.8.8.8/dns-query", "detour": "direct"}
            ],
            "final": "google"
        },
        "inbounds": [
            {
                "type": "tun",
                "tag": "tun-in",
                "inet4_address": "172.19.0.1/30",
                "auto_route": True,
                "strict_route": True,
                "stack": "system",
                "sniff": True
            }
        ],
        "outbounds": outbounds + [
            {"type": "direct", "tag": "direct"},
            {"type": "block", "tag": "block"},
            {"type": "dns", "tag": "dns-out"}
        ],
        "route": {
            "rules": [
                {"protocol": "dns", "outbound": "dns-out"}
            ],
            "final": "direct"
        }
    }
    
    return json.dumps(config, ensure_ascii=False, indent=2)
