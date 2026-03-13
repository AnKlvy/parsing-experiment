from playwright.async_api import async_playwright, ViewportSize


async def get_browser_context(proxy: dict | None = None):
    playwright = await async_playwright().start()

    # browser = await playwright.chromium.launch(headless=True,
    #                                            args=[
    #                                                "--disable-blink-features=AutomationControlled",
    #                                                "--disable-dev-shm-usage",
    #                                                "--no-sandbox",
    #                                                # "--disable-web-security",
    #                                                # "--disable-features=VizDisplayCompositor"
    #                                            ],
    #                                            # slow_mo=50
    #                                            )
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir="data/profile",
        # proxy=proxy,
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
        viewport=ViewportSize(width=1920, height=1080),
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        java_script_enabled=True,
        ignore_https_errors=True,
    )

    # context = await browser.new_context(
    #     proxy=proxy,
    #     viewport=ViewportSize(width=1920, height=1080),
    #     user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    #     java_script_enabled=True,
    #     ignore_https_errors=True,
    # )

    # await context.add_init_script("""
    #             Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    #             Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    #         """)

    return playwright, context
