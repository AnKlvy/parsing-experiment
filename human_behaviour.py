import asyncio
import random


async def human_delay(min_s=1.0, max_s=3.0):
    await asyncio.sleep(random.uniform(min_s, max_s))

async def simulate_human(page):
    width = 1920
    height = 1080

    # Движения мыши
    for _ in range(random.randint(3, 6)):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        await page.mouse.move(x, y, steps=random.randint(10, 25))
        await human_delay(0.2, 0.8)

    # Скролл вниз
    for _ in range(random.randint(2, 5)):
        await page.mouse.wheel(0, random.randint(300, 800))
        await human_delay(0.5, 1.5)

    # Немного вверх
    await page.mouse.wheel(0, -random.randint(200, 500))
    await human_delay(1.0, 2.0)

async def warmup_session(context, url):
    page = await context.new_page()

    page.set_default_timeout(15000)
    page.set_default_navigation_timeout(50000)
    # Открываем главную
    response = await page.goto(url)

    # Даем JS полностью выполниться
    await human_delay()

    # Имитация поведения
    await simulate_human(page)

    # Подождать ещё чуть-чуть
    await human_delay(2, 4)

    return page, response