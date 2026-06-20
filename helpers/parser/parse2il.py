import base64
import re
from urllib.parse import urlparse, parse_qs, unquote, quote
from helpers.parser.schemes.il import ILNode, ILSubscription

def _is_base32(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    return bool(re.match(r'^[A-Z2-7]+=*$', text)) and len(text) > 20


def _is_stub_response(decoded_text: str) -> tuple[bool, str]:
    text_lower = decoded_text.lower()
    
    if "@0.0.0.0:1" in decoded_text or "@127.0.0.1:1" in decoded_text:
        if "limit" in text_lower or "device" in text_lower:
            return True, "Лимит устройств достигнут"
        return True, "Фейковая нода (0.0.0.0)"
    
    if "@0.0.0.0:" in decoded_text:
        return True, "Фейковая нода (0.0.0.0)"

    ru_keywords = {
        "деактивирован": "Подписка деактивирована",
        "деактивирована": "Подписка деактивирована",
        "деактивировано": "Подписка деактивирована",
        "отключен": "Подписка отключена",
        "отключена": "Подписка отключена",
        "отключено": "Подписка отключена",
        "заблокирован": "Подписка заблокирована",
        "заблокирована": "Подписка заблокирована",
        "приостановлен": "Подписка приостановлена",
        "приостановлена": "Подписка приостановлена",
        "истек": "Срок подписки истёк",
        "истекла": "Срок подписки истёк",
        "истекло": "Срок подписки истёк",
        "неактивен": "Подписка неактивна",
        "не активен": "Подписка неактивна",
        "исчерпан": "Лимит исчерпан",
        "исчерпана": "Лимит исчерпан",
        "лимит устройств": "Лимит устройств достигнут",
        "лимит исчерпан": "Лимит исчерпан",
        "подписка недействительна": "Подписка недействительна",
        "доступ запрещен": "Доступ запрещён",
        "доступ заблокирован": "Доступ заблокирован",
    }
    
    for keyword, reason in ru_keywords.items():
        if keyword in text_lower:
            return True, reason

    en_keywords = {
        "limit of devices": "Device limit reached",
        "device limit reached": "Device limit reached",
        "too many devices": "Too many devices",
        "subscription expired": "Subscription expired",
        "trial ended": "Trial period ended",
        "no active subscription": "No active subscription",
        "account suspended": "Account suspended",
        "quota exceeded": "Quota exceeded",
        "deactivated": "Subscription deactivated",
        "deactive": "Subscription deactivated",
        "disabled": "Subscription disabled",
        "blocked": "Subscription blocked",
        "suspended": "Subscription suspended",
        "revoked": "Subscription revoked",
        "inactive": "Subscription inactive",
        "not active": "Subscription not active",
        "exhausted": "Limit exhausted",
        "access denied": "Access denied",
        "access blocked": "Access blocked",
        "subscription canceled": "Subscription canceled",
        "subscription terminated": "Subscription terminated",
    }
    
    for keyword, reason in en_keywords.items():
        if keyword in text_lower:
            return True, reason
            
    return False, ""

def _generate_stub_nodes(reason: str = "") -> list:
    title_node = ILNode(
        protocol="vless",
        name="v2tetotech // device limited",
        server="0.0.0.0",
        port=1,
        uuid="00000000-0000-0000-0000-000000000000",
        network="tcp",
        security="none",
        flow="",
        sni="",
        fp="",
        pbk="",
        sid="",
        path="",
        host="",
        alpn=[],
        extra={"warning": True, "type": "title"}
    )

    description = "Провайдер ограничил подписку; до v2tetotech уже был исчерпан лимит"
    if reason:
        description = f"Причина: {reason}; провайдер ограничил подписку до v2tetotech"
    
    desc_node = ILNode(
        protocol="vless",
        name=description,
        server="0.0.0.0",
        port=1,
        uuid="00000000-0000-0000-0000-000000000000",
        network="tcp",
        security="none",
        flow="",
        sni="",
        fp="",
        pbk="",
        sid="",
        path="",
        host="",
        alpn=[],
        extra={"warning": True, "type": "description"}
    )
    
    return [title_node, desc_node]

def _decode_v2plus_codec(raw: str) -> str | None:
    # Крутейшее "шифрование" yaenot/v2plus
    try:
        b32_str = raw.upper().strip()
        b32_str += '=' * (-len(b32_str) % 8)
        step1_bytes = base64.b32decode(b32_str)
        step1_str = step1_bytes.decode('utf-8')
        
        step1_str += '=' * (-len(step1_str) % 4)
        step2_bytes = base64.b64decode(step1_str)
        final_text = step2_bytes.decode('utf-8')
        
        if "://" in final_text:
            return final_text
        return None
    except Exception:
        return None


def _decode_standard(raw: str) -> str:
    try:
        padded = raw.strip() + '=' * (-len(raw.strip()) % 4)
        return base64.b64decode(padded).decode('utf-8')
    except Exception:
        return raw

def parse_to_il(raw_sub: str, client_ua: str = "", target_url: str = "") -> ILSubscription:
    decoded = None
    
    if "yaenot.xyz" in target_url:
        decoded = _decode_v2plus_codec(raw_sub)
        
    if not decoded and ("v2plus" in client_ua.lower() or _is_base32(raw_sub)):
        decoded = _decode_v2plus_codec(raw_sub)
        
    if not decoded:
        decoded = _decode_standard(raw_sub)
    
    is_stub, reason = _is_stub_response(decoded)
    if is_stub:
        print(f"\n[⚠️ STUB DETECTED] Provider returned fake stub!")
        print(f"[⚠️ REASON] {reason}")
        print(f"[⚠️ RAW RESPONSE] {decoded[:200]}...\n")
        
        stub_nodes = _generate_stub_nodes(reason)
        return ILSubscription(nodes=stub_nodes)
    
    nodes = []
    for line in decoded.splitlines():
        line = line.strip()
        if not line:
            continue
        
        if "@0.0.0.0" in line or "@127.0.0.1" in line:
            continue
            
        if line.startswith("vless://"):
            try:
                p = urlparse(line)
                q = parse_qs(p.query)
                nodes.append(ILNode(
                    protocol="vless",
                    name=unquote(p.fragment) if p.fragment else "",
                    uuid=p.username or "",
                    server=p.hostname or "",
                    port=p.port or 443,
                    flow=q.get("flow", [""])[0],
                    network=q.get("type", ["tcp"])[0],
                    security=q.get("security", ["tls"])[0],
                    sni=q.get("sni", [""])[0],
                    fp=q.get("fp", ["chrome"])[0],
                    pbk=q.get("pbk", [""])[0],
                    sid=q.get("sid", [""])[0],
                    path=q.get("path", [""])[0],
                    host=q.get("host", [""])[0],
                    alpn=q.get("alpn", [""])[0].split(",") if q.get("alpn") else []
                ))
            except Exception as e:
                print(f"[WARN] Failed to parse vless: {e}")
        
        elif line.startswith("vmess://"):
            try:
                import json
                b64 = line.replace("vmess://", "")
                padded = b64 + '=' * (-len(b64) % 4)
                data = json.loads(base64.b64decode(padded).decode('utf-8'))
                nodes.append(ILNode(
                    protocol="vmess",
                    name=data.get("ps", ""),
                    server=data.get("add", ""),
                    port=int(data.get("port", 443)),
                    uuid=data.get("id", ""),
                    network=data.get("net", "tcp"),
                    security=data.get("tls", "none"),
                    sni=data.get("sni", ""),
                    path=data.get("path", ""),
                    host=data.get("host", ""),
                    extra={"aid": data.get("aid", 0), "scy": data.get("scy", "auto")}
                ))
            except Exception as e:
                print(f"[WARN] Failed to parse vmess: {e}")
        
        elif line.startswith("trojan://"):
            try:
                p = urlparse(line)
                q = parse_qs(p.query)
                nodes.append(ILNode(
                    protocol="trojan",
                    name=unquote(p.fragment) if p.fragment else "",
                    uuid=p.username or "",
                    server=p.hostname or "",
                    port=p.port or 443,
                    sni=q.get("sni", [q.get("peer", [""])[0]])[0],
                    network=q.get("type", ["tcp"])[0]
                ))
            except Exception as e:
                print(f"[WARN] Failed to parse trojan: {e}")
        
        elif line.startswith("ss://"):
            try:
                body = line.replace("ss://", "").split("#")[0]
                name = unquote(line.split("#")[1]) if "#" in line else ""
                padded = body + '=' * (-len(body) % 4)
                decoded_ss = base64.b64decode(padded).decode('utf-8')
                method, rest = decoded_ss.split(":", 1)
                server, port = rest.rsplit("@", 1)
                host, port = port.split(":", 1) if ":" in port else (port, "443")
                nodes.append(ILNode(
                    protocol="ss",
                    name=name,
                    method=method,
                    uuid=server,
                    server=host,
                    port=int(port)
                ))
            except Exception as e:
                print(f"[WARN] Failed to parse ss: {e}")
    
    return ILSubscription(nodes=nodes)
