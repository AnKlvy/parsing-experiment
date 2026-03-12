import asyncio
import json
from pathlib import Path
from playwright.async_api import BrowserContext


COOKIES_PATH = Path("cookies.json")


async def save_cookies(context: BrowserContext) -> None:
    cookies = await context.cookies()
    COOKIES_PATH.write_text(json.dumps(cookies, indent=2))


def load_cookies() -> list[dict]:
    if not COOKIES_PATH.exists():
        return []
    return json.loads(COOKIES_PATH.read_text())

from urllib.parse import urlparse

def build_cookies_for_url(cookies_raw: list[dict], url: str) -> dict[str, str]:
    hostname = urlparse(url).hostname

    return {
        cookie["name"]: cookie["value"]
        for cookie in cookies_raw
        if hostname.endswith(cookie.get("domain", "").lstrip("."))
    }

async def wait_for_cookie(context, cookie_name: str, timeout: int = 10000):
    import time
    start = time.time()

    while True:
        cookies = await context.cookies()
        if any(c["name"] == cookie_name for c in cookies):
            return

        if (time.time() - start) * 1000 > timeout:
            raise TimeoutError(f"{cookie_name} not set")

        await asyncio.sleep(0.2)