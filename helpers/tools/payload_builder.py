import base64
from data.config import DEFAULT_SPOOF_PROFILE, SPOOF_FALLBACK_CHAIN
from helpers.tools.hwid_gen import generate_hwid_from_url

def get_optimal_profile(strategy: str = "best", url: str = None) -> dict:
    profile = DEFAULT_SPOOF_PROFILE.copy()
    
    if url:
        profile["hwid"] = generate_hwid_from_url(url)
    else:
        profile["hwid"] = "0000000000000000"
        
    profile["chain"] = ",".join(SPOOF_FALLBACK_CHAIN)
    return profile

def build_payload_string(params: dict) -> str:
    parts = []
    for k, v in params.items():
        if v is None: continue
        val_str = str(v)
        if val_str.lower() not in ("default", "none", "null", ""):
            parts.append(f"{k}={val_str}")
    return ",".join(parts)

def build_payload_b64(params: dict) -> str:
    payload_str = build_payload_string(params)
    return base64.urlsafe_b64encode(payload_str.encode('utf-8')).decode('utf-8')

def generate_v2tetotech_link(
    base_url: str, sub_url: str, strategy: str = "best", custom_params: dict = None
) -> dict:
    profile = get_optimal_profile(strategy, url=sub_url)
    profile["link"] = sub_url
    
    if custom_params:
        for k, v in custom_params.items():
            if v and str(v).lower() not in ("default", "none", "null", ""):
                profile[k] = v

    payload_str = build_payload_string(profile)
    payload_b64 = base64.urlsafe_b64encode(payload_str.encode('utf-8')).decode('utf-8')
    advsync_url = f"{base_url.rstrip('/')}/advsync?p={payload_b64}"

    deeplinks = {
        "v2rayng": f"v2rayng://install-sub?url={advsync_url}",  # v2rayNG
        "clash": f"clash://install-config?url={advsync_url}",  # clash
        "singbox": f"sing-box://import-remote-profile?url={advsync_url}",  # sfa (sing-box for android)
        "nekobox": f"nekobox://import-remote-profile?url={advsync_url}",  # NekoBox
        "happ": f"happ://import/{advsync_url}",  # Happ
    }

    return {
        "strategy_used": strategy,
        "selected_profile": profile,
        "payload_string": payload_str,
        "payload_base64": payload_b64,
        "v2tetotech_link": advsync_url,
        "deeplinks": deeplinks,
    }
