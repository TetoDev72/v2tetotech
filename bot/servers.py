import asyncio
import time
from typing import Optional, Dict, List
from dataclasses import dataclass
import httpx
from datetime import datetime, timedelta


@dataclass
class ServerStatus:
    url: str
    available: bool
    latency_ms: Optional[float] = None
    last_check: Optional[datetime] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "available": self.available,
            "latency_ms": self.latency_ms,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "error": self.error
        }


class ServerManager:
    SERVERS = [
        "localhost:8000"
    ]
    CHECK_TIMEOUT = 5.0
    CACHE_TTL = 300

    def __init__(self):
        self._cache: Dict[str, ServerStatus] = {}
        self._last_full_check: Optional[datetime] = None

    async def check_server(self, url: str) -> ServerStatus:
        if url in self._cache:
            cached = self._cache[url]
            if cached.last_check and (datetime.now() - cached.last_check).total_seconds() < self.CACHE_TTL:
                return cached

        healthcheck_url = f"{url}/svinfo"
        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=self.CHECK_TIMEOUT) as client:
                response = await client.get(healthcheck_url)

                if response.status_code == 200:
                    latency = (time.time() - start_time) * 1000  # ms

                    status = ServerStatus(
                        url=url,
                        available=True,
                        latency_ms=round(latency, 2),
                        last_check=datetime.now(),
                        error=None
                    )
                else:
                    status = ServerStatus(
                        url=url,
                        available=False,
                        latency_ms=None,
                        last_check=datetime.now(),
                        error=f"HTTP {response.status_code}"
                    )

        except httpx.TimeoutException:
            status = ServerStatus(
                url=url,
                available=False,
                latency_ms=None,
                last_check=datetime.now(),
                error="Timeout"
            )

        except Exception as e:
            status = ServerStatus(
                url=url,
                available=False,
                latency_ms=None,
                last_check=datetime.now(),
                error=str(e)
            )

        self._cache[url] = status
        return status

    async def check_all_servers(self) -> List[ServerStatus]:
        tasks = [self.check_server(url) for url in self.SERVERS]
        results = await asyncio.gather(*tasks)

        self._last_full_check = datetime.now()
        return results

    async def get_best_server(self) -> Optional[str]:
        statuses = await self.check_all_servers()
        available = [s for s in statuses if s.available and s.latency_ms is not None]

        if not available:
            return None

        available.sort(key=lambda s: s.latency_ms)

        return available[0].url

    async def get_working_server(self) -> Optional[str]:
        statuses = await self.check_all_servers()

        for status in statuses:
            if status.available:
                return status.url

        return None

    async def get_server_status_text(self) -> str:
        statuses = await self.check_all_servers()

        lines = ["🖥 **Статус серверов v2tetotech:**\n"]

        for status in statuses:
            if status.available:
                emoji = "✅"
                latency_str = f"{status.latency_ms:.0f}ms" if status.latency_ms else "N/A"
                line = f"{emoji} {status.url}\n   ⏱ {latency_str}"
            else:
                emoji = "❌"
                error_str = status.error or "Unknown error"
                line = f"{emoji} {status.url}\n   ⚠️ {error_str}"

            lines.append(line)

        best = await self.get_best_server()
        if best:
            lines.append(f"\n🏆 **Лучший сервер:** {best}")
        else:
            lines.append("\n⚠️ **Все сервера недоступны!**")

        return "\n".join(lines)

    async def get_server_for_user(self) -> Optional[str]:
        best = await self.get_best_server()
        if best:
            return best

        working = await self.get_working_server()
        if working:
            return working

        return None

server_manager = ServerManager()
