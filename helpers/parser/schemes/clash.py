import yaml
from helpers.parser.schemes.il import ILSubscription

def to_clash_yaml(il: ILSubscription) -> str:
    proxies = []
    proxy_names = []
    
    for n in il.nodes:
        if n.protocol == "vless":
            proxy = {
                "name": n.name or f"VLESS-{n.server}",
                "type": "vless",
                "server": n.server,
                "port": n.port,
                "uuid": n.uuid,
                "network": n.network or "tcp",
                "tls": True,
                "udp": True,
                "client-fingerprint": n.fp or "chrome"
            }
            if n.flow: proxy["flow"] = n.flow
            if n.sni: proxy["servername"] = n.sni
            
            if n.security == "reality" and n.pbk:
                proxy["reality-opts"] = {
                    "public-key": n.pbk,
                    "short-id": n.sid or ""
                }
                
            if n.network == "ws" and n.path:
                proxy["ws-opts"] = {"path": n.path, "headers": {"Host": n.host}}
            elif n.network == "grpc" and n.path:
                proxy["grpc-opts"] = {"grpc-service-name": n.path}
                
            proxies.append(proxy)
            proxy_names.append(proxy["name"])
            
        elif n.protocol == "trojan":
            proxy = {
                "name": n.name or f"Trojan-{n.server}",
                "type": "trojan",
                "server": n.server,
                "port": n.port,
                "password": n.uuid,
                "udp": True
            }
            if n.sni: proxy["sni"] = n.sni
            proxies.append(proxy)
            proxy_names.append(proxy["name"])

    config = {
        "mixed-port": 7890,
        "allow-lan": False,
        "mode": "rule",
        "log-level": "info",
        "unified-delay": True,
        "tcp-concurrent": True,
        "proxies": proxies,
        "proxy-groups": [
            {
                "name": "PROXY",
                "type": "select",
                "proxies": proxy_names + ["DIRECT"]
            }
        ],
        "rules": [
            "MATCH,PROXY"
        ]
    }
    
    return yaml.dump(config, allow_unicode=True, sort_keys=False, default_flow_style=False)
