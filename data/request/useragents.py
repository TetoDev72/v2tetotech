HAPP_VERSION = "3.19.0"

def get_happ_ua(os_name: str = "Android") -> str:
    os_lower = os_name.lower().strip()

    if os_lower in ("android", "a", ""):
        return f"Happ/{HAPP_VERSION}"
    elif os_lower in ("ios", "iphone", "ipad"):
        return f"Happ/{HAPP_VERSION}/ios"
    elif os_lower in ("windows", "win", "win32", "nt"):
        return f"Happ/{HAPP_VERSION}/windows"
    elif os_lower in ("macos", "mac", "darwin", "osx"):
        return f"Happ/{HAPP_VERSION}/macos"
    else:
        return f"Happ/{HAPP_VERSION}"

CLIENT_UAS = {
    "happ": f"Happ/{HAPP_VERSION}",
    "v2plus": "v2plus/1.4.2",
    "v2rayng": "V2rayNG/1.9.15",
    "v2rayn": "v2rayN/7.5.4",
    "nekobox": "NekoBox/1.3.1",
    "clash": "ClashForAndroid/2.5.12",
    "mihomo": "mihomo/1.19.0",
    "singbox": "SFI/1.11.0",
    "sfa": "SFA/1.11.0",
    "hiddify": "HiddifyNext/2.5.7",
    "shadowrocket": "Shadowrocket/2.2.6",
    "stash": "Stash/3.0.4",
    "streisand": "Streisand/1.6.23",
    "foxray": "FoXray/3.0.0",
}

BROWSER_UAS = {
    "chrome": "Mozilla/5.0 (Linux; Android 15; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "firefox": "Mozilla/5.0 (Android 15; Mobile; rv:133.0) Gecko/133.0 Firefox/133.0",
    "safari": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1",
    "edge": "Mozilla/5.0 (Linux; Android 15; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 EdgA/131.0.0.0",
}

def get_ua(client: str = "happ", os_name: str = "Android") -> str:
    client_lower = client.lower().strip()

    if client_lower in ("happ", "happ://"):
        return get_happ_ua(os_name)

    if client_lower in CLIENT_UAS:
        return CLIENT_UAS[client_lower]
    if client_lower in BROWSER_UAS:
        return BROWSER_UAS[client_lower]

    return client
