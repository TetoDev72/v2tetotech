import httpx
import logging
from config import API_BASE, TIMEOUT

logger = logging.getLogger(__name__)

class V2TTClient:
    def __init__(self, base_url: str = API_BASE, timeout: float = TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout

    async def call(self, cmd: str, data: dict, server: str = None) -> dict:
        target_server = server or self.base_url
        url = f"{target_server}/api"
        payload = {"cmd": cmd, "role": "REQUEST", "data": data}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                resp_json = response.json()

                return resp_json.get("data", resp_json)

        except httpx.HTTPStatusError as e:
            logger.error(f"API Error {e.response.status_code} for {cmd}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Connection error for {cmd}: {e}")
            raise

v2tt = V2TTClient()
