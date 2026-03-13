import asyncio
from pathlib import Path

from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import ProxyError
from browser import get_browser_context
from cookies import build_cookies_for_url, save_cookies
from human_behaviour import warmup_session


def parse_proxy(proxy_url: str) -> dict:
    from urllib.parse import urlparse

    parsed = urlparse(proxy_url)

    return {
        "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
        "username": parsed.username,
        "password": parsed.password,
    }


# WEBSITE_URL = 'https://exhibitors.vitafoods.eu.com/live/figlobal/event46.jsp?site=47&type=company&eventid=598&map=false&name=&SugType_val=&RecordId_val='
COMPANIES_URL = 'https://exhibitors.vitafoods.eu.com/live/search/search_exhibition46json.jsp?v=25&site=47&type=company&eventid=598&name=%25&eventid=598&types=all'

# app/services/requests_service.py

import json

async def async_requests(
        url: str,
        cookies: dict[str, str] = None,
        headers: dict[str, str] = None,
        params: dict[str, str] = None,
        proxy_raw: str = None
) -> list[dict]:

    async with AsyncSession(base_url=url) as session:
        try:
            response = await session.post(
                url=url,
                headers=headers,
                cookies=cookies,
            )

        except ProxyError as e:
            print("Invalid proxy: ", str(e)[:500])
            return []

        except Exception as e:
            print("Unexpected curl cffi error:", str(e)[:500])
            return []

        print(response.status_code)

        raw_text = response.text

        json_start = raw_text.find("{")
        if json_start == -1:
            return []

        json_data = json.loads(raw_text[json_start:])
        results = json_data.get("results", [])

        print(f"companies found: {len(results)}")

        # сохранение
        output_path = Path("data/companies.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        return results
async def playwright_request(url, proxy=None):
    playwright, context = await get_browser_context(proxy)

    try:
        try:
            # page, response = await warmup_session(context, url)
            page = await context.new_page()
            response = await page.goto(url)
        except:
            return None, None

        cookies_raw = await context.cookies()
        cookies = build_cookies_for_url(cookies_raw, url)

        print(cookies)
        print("status:", response.status if response else None)
        await save_cookies(context)
        user_agent = await page.evaluate("navigator.userAgent")
        print(user_agent)

        if not response or response.status != 200:
            return None, None

        return cookies, user_agent

    finally:
        await context.close()
        await playwright.stop()


async def main():
    cookies, user_agent = await playwright_request(COMPANIES_URL)
    headers = {'user-agent': user_agent}


    for _ in range(10000):
        await async_requests(url=COMPANIES_URL,
                             cookies=cookies,
                             headers=headers,
                             # params=params,
                             # proxy_raw=proxy_raw,
                             )
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
