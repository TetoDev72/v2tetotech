import base64
from helpers.crypt import happcrypt, happcrypt5


def safe_b64decode(s: str) -> str:
    s += '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s).decode('utf-8')


async def resolve_link(raw_link: str) -> str:
    link = raw_link.strip()
    
    try:
        decoded = safe_b64decode(link)
        if decoded.startswith(("http://", "https://", "happ://")):
            link = decoded
    except Exception:
        pass
    
    if link.startswith("happ://"):
        if "crypt5/" in link:
            link = await happcrypt5.decrypt(link)
        else:
            link = await happcrypt.decrypt(link)
    
    if not link.startswith(("http://", "https://")):
        raise ValueError(f"Invalid link: {link[:50]}...")
    
    return link
