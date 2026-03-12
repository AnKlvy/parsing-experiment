import asyncio

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


WEBSITE_URL = 'https://exhibitors.vitafoods.eu.com/live/figlobal/event46.jsp?site=47&type=company&eventid=598&map=false&name=&SugType_val=&RecordId_val='


async def async_requests(url: str, cookies: dict[str, str] = None, headers: dict[str, str] = None,
                         params: dict[str, str] = None,
                         proxy_raw: str = None) -> list[
    dict[str, str]]:
    async with AsyncSession(base_url=url) as session:
        try:
            response = await session.post(url=url,
                                          # params=params,
                                          # headers=headers,
                                          # cookies=cookies,
                                          # proxy=proxy_raw,
                                          # data=json_data
                                          )
        except ProxyError as e:
            print("Invalid proxy: ", e.__str__()[:500])
            return []
        except Exception as e:
            print("Unexpected curl cffi error:", e.__str__()[:500])
            return []
        print(response.status_code)

        cookies_dict = dict(response.cookies.items())

        print("cookies:", cookies_dict)

        print("response from cffi: ", response.text[:1000])
        if response.status_code == 200:
            print("Successful proxy: {}".format(proxy_raw))

        return response


async def playwright_request(url, proxy=None):
    playwright, context = await get_browser_context(proxy)

    try:
        try:
            page, response = await warmup_session(context, url)
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
    cookies, user_agent = await playwright_request(WEBSITE_URL)
    headers = {'user-agent': user_agent}


    await async_requests(url=WEBSITE_URL,
                         cookies=cookies,
                         headers=headers,
                         # params=params,
                         # proxy_raw=proxy_raw,
                         )
    await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
