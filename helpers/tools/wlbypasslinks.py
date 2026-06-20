import urllib.parse

STRATEGIES = {
    "yandex_translate": {
        "name": "Yandex Translate",
        "description": "Оборачивает ссылку в translate.yandex.ru (всегда в белом списке РКН)",
        "template": "https://translate.yandex.ru/translate?url={url}&lang=de-de",
    },
}


def list_strategies() -> dict:
    return {k: {"name": v["name"], "description": v["description"]}
            for k, v in STRATEGIES.items()}


def apply_bypass(url: str, strategy: str = "yandex_translate") -> dict:
    if not url:
        return {"success": False, "error": "Empty URL", "strategy": strategy}

    if strategy not in STRATEGIES:
        return {
            "success": False,
            "error": f"Unknown strategy '{strategy}'. Available: {list(STRATEGIES.keys())}",
            "strategy": strategy,
        }

    strategy_data = STRATEGIES[strategy]
    encoded_url = urllib.parse.quote(url, safe='')
    bypass_url = strategy_data["template"].format(url=encoded_url)

    return {
        "success": True,
        "original_url": url,
        "bypass_url": bypass_url,
        "strategy": strategy,
        "strategy_name": strategy_data["name"],
    }
