import base64

def rebrand(raw_sub: str, brand: dict = None, mode: str = None) -> str:
    clean_brand = {}
    if brand:
        clean_brand = {k: v for k, v in brand.items() if v and str(v).lower() not in ("default", "none", "null", "")}

    if not clean_brand:
        return raw_sub

    headers = []
    if clean_brand.get("title"):
        b64_title = base64.b64encode(clean_brand["title"].encode('utf-8')).decode('utf-8')
        headers.append(f"//profile-title: base64:{b64_title}")
    if clean_brand.get("updateint"):
        headers.append(f"//profile-update-interval: {clean_brand['updateint']}")
    if clean_brand.get("webpage"):
        headers.append(f"//profile-web-page-url: {clean_brand['webpage']}")
    if clean_brand.get("lastupd"):
        headers.append(f"//last update on: {clean_brand['lastupd']}")
    if clean_brand.get("announce"):
        headers.append(f"//announce: {clean_brand['announce']}")

    if not headers:
        return raw_sub

    try:
        padded = raw_sub.strip() + '=' * (-len(raw_sub.strip()) % 4)
        decoded = base64.b64decode(padded).decode('utf-8')
        merged = "\n".join(headers) + "\n" + decoded
        return base64.b64encode(merged.encode('utf-8')).decode('utf-8')
    except Exception:
        return "\n".join(headers) + "\n" + raw_sub
