"""
v2tetotechclient.py
Полноценный асинхронный Python-клиент для API v2tetotech.
Поддерживает как JSON API (POST /api), так и REST эндпоинты для получения сырых подписок.

Зависимости: httpx (pip install httpx)

Пример использования:
    async with V2TetoClient("http://localhost:8000") as client:
        # 1. Получаем информацию о сервере
        info = await client.server_info()
        print(f"Сервер: {info['name']} v{info['version']}")

        # 2. Генерируем диплинк для v2rayng
        deeplink = await client.get_deeplink("https://example.com/sub", client="v2rayng")
        print(f"Диплинк: {deeplink['deeplink']}")

        # 3. Получаем сырую подписку через REST
        raw_sub = await client.get_auto_sub("https://example.com/sub")
        print(f"Сырая подписка (первые 50 символов): {raw_sub[:50]}...")
"""

import httpx
from typing import Optional, Dict, Any, List, Union

class V2TetoError(Exception):
    """Базовый класс для ошибок v2tetotech API."""
    pass

class V2TetoClient:
    """
    Асинхронный клиент для v2tetotech API.

    Args:
        base_url (str): Базовый URL сервера v2tetotech (например, "http://localhost:8000").
        timeout (float): Таймаут запросов в секундах.
    """

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    # ====================================================================================
    # 🛠 Внутренние методы
    # ====================================================================================

    async def _api_call(self, cmd: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Делает POST запрос к /api и автоматически распаковывает поле 'data' из ответа."""
        if not self._client:
            raise V2TetoError("Client is not initialized. Use 'async with V2TetoClient(...) as client:'")

        payload = {
            "cmd": cmd,
            "role": "REQUEST",
            "data": data or {}
        }

        response = await self._client.post("/api", json=payload)
        response.raise_for_status()

        resp_json = response.json()
        if resp_json.get("role") == "RESPONSE":
            return resp_json.get("data", {})

        raise V2TetoError(f"Unexpected response role: {resp_json.get('role')}")

    # ====================================================================================
    # 🚀 JSON API Commands (POST /api)
    # ====================================================================================

    async def ping(self) -> Dict[str, Any]:
        """Проверка доступности сервера (PING)."""
        return await self._api_call("PING")

    async def server_info(self) -> Dict[str, Any]:
        """Получение информации о сервере, версии и зеркалах (SERVER_INFO)."""
        return await self._api_call("SERVER_INFO")

    async def get_hwid(self, url: str) -> Dict[str, Any]:
        """Генерация предсказуемого HWID (CRC-16) для ссылки (HWID)."""
        return await self._api_call("HWID", {"url": url})

    async def decrypt(self, link: str) -> Dict[str, Any]:
        """Дешифровка happ://crypt* ссылок (DECRYPT)."""
        return await self._api_call("DECRYPT", {"link": link})

    async def get_headers(self) -> Dict[str, Any]:
        """
        Получение заголовков клиента в виде vless:// ключей (HEADERS).
        Примечание: Сервер читает заголовки самого HTTP-запроса от этого клиента.
        """
        return await self._api_call("HEADERS")

    async def get_device(self) -> Dict[str, Any]:
        """Получение данных устройства из заголовков (DEVICE)."""
        return await self._api_call("DEVICE")

    async def get_deeplink(
        self,
        url: str,
        client: str = "v2rayng",
        mode: str = "sync",
        base_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Создание диплинков для различных клиентов (DEEPLINK).

        Args:
            url: Исходная ссылка на подписку.
            client: Целевой клиент (v2rayng, clash, singbox, nekobox, hiddify и т.д.).
            mode: Режим (sync, fetch, advsync).
            base_url: Базовый URL для генерации ссылки (если отличается от текущего).
        """
        data = {"url": url, "client": client, "mode": mode}
        if base_url:
            data["base_url"] = base_url
        return await self._api_call("DEEPLINK", data)

    async def charity(self) -> Dict[str, Any]:
        """Получение благотворительной подписки от v2tetotech (CHARITY)."""
        return await self._api_call("CHARITY")

    async def batch(self, urls: List[str]) -> Dict[str, Any]:
        """Склейка нескольких подписок в одну (BATCH)."""
        return await self._api_call("BATCH", {"urls": ",".join(urls)})

    async def sync_sub(self, url: str, hwid: str = "default", client: str = "happ") -> Dict[str, Any]:
        """Получение подписки с авто HWID и спуфингом (SYNC)."""
        return await self._api_call("SYNC", {"url": url, "hwid": hwid, "client": client})

    async def fetch_sub(self, url: str, client: str = "auto") -> Dict[str, Any]:
        """Получение подписки без спуфинга, с конвертацией формата (FETCH)."""
        return await self._api_call("FETCH", {"url": url, "client": client})

    async def advanced_sync(self, link: str, **kwargs) -> Dict[str, Any]:
        """
        Продвинутый SYNC с полным контролем над параметрами (ADVANCED_SYNC).

        Args:
            link: Ссылка на подписку.
            **kwargs: Любые параметры payload data (hwid, ua, os, model, title, format, chain и т.д.).
        """
        data = {"link": link}
        data.update(kwargs)
        return await self._api_call("ADVANCED_SYNC", data)

    async def payload_gen(
        self,
        link: str,
        strategy: str = "best",
        base_url: Optional[str] = None,
        mode: str = "sync"
    ) -> Dict[str, Any]:
        """Генерация готовой ссылки advsync с зашитым payload и набором диплинков (PAYLOAD_GEN)."""
        data = {"link": link, "strategy": strategy, "mode": mode}
        if base_url:
            data["base_url"] = base_url
        return await self._api_call("PAYLOAD_GEN", data)

    async def whitelist_bypass(self, url: str, strategy: str = "yandex_translate") -> Dict[str, Any]:
        """Обертывание ссылки для обхода whitelist блокировок (WHITELIST_BYPASS_LINK)."""
        return await self._api_call("WHITELIST_BYPASS_LINK", {"url": url, "strategy": strategy})

    # ====================================================================================
    # 🌐 REST Endpoints (Получение сырых данных / конфигов)
    # ====================================================================================

    async def get_auto_sub(self, link: str) -> str:
        """Получение сырой подписки через /auto (маскировка под Happ, авто HWID)."""
        resp = await self._client.get(f"/auto/{link}")
        resp.raise_for_status()
        return resp.text

    async def get_fetch_sub(self, link: str) -> str:
        """Получение подписки через /fetch (конвертация в Clash/Sing-box/Xray по User-Agent)."""
        resp = await self._client.get(f"/fetch/{link}")
        resp.raise_for_status()
        return resp.text

    async def get_sync_sub(self, encoded_link: str) -> str:
        """Получение подписки через /sync (формат определяется по User-Agent)."""
        resp = await self._client.get(f"/sync/{encoded_link}")
        resp.raise_for_status()
        return resp.text

    async def get_charity_sub(self) -> str:
        """Получение сырой charity подписки."""
        resp = await self._client.get("/charity")
        resp.raise_for_status()
        return resp.text

    async def get_batch_sub(self, urls: List[str]) -> str:
        """Получение склеенной сырой подписки."""
        resp = await self._client.get("/batch", params={"urls": ",".join(urls)})
        resp.raise_for_status()
        return resp.text

    async def get_svinfo_text(self) -> str:
        """Получение информации о сервере в виде текста."""
        resp = await self._client.get("/svinfo")
        resp.raise_for_status()
        return resp.text

    async def get_spoof_data(self, strategy: str = "best") -> Dict[str, Any]:
        """Получение дефолтных данных спуфинга."""
        resp = await self._client.get("/spoofdata", params={"strategy": strategy})
        resp.raise_for_status()
        return resp.json()

    async def get_headers_rest(self) -> Dict[str, Any]:
        """Получение заголовков через REST GET /headers."""
        resp = await self._client.get("/headers")
        resp.raise_for_status()
        return resp.json()
