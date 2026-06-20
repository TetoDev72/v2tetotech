def parse_payload(p_str: str) -> dict:
    res = {}
    if not p_str: return res
    sep = '&' if '&' in p_str and ',' not in p_str else ','
    for pair in p_str.split(sep):
        pair = pair.strip()
        if not pair or '=' not in pair: continue
        k, v = pair.split('=', 1)
        key = k.strip().lower()
        value = v.strip()
        
        valid_keys = {
            "hwid", "ua", "os", "model", "osver", "realip", "forwardedfor",
            "brand", "advanced", "link", "format", "spoof", "client",
            "title", "updateint", "webpage", "lastupd", "announce", "chain"
        }
        if key in valid_keys and value:
            res[key] = value
    return res
