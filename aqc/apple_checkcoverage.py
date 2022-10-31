from aioconsole import ainput
from aiohttp import ClientSession
from asyncio import sleep, to_thread

from .captcha_db import get_solver, erase_captcha
from .get_apple_info import get_apple_info
from .get_cookies import get_cookies
from .headers import headers


def generate_data(serial: str, captcha: str, captchaMode: str='audio') -> str:
    return {"sno": serial, "ans": captcha, "captchaMode": captchaMode, "CSRFToken": "null"}


# бесконечный цикл проверки серийного номера
async def apple_checkcoverage():
    print("Quick check Apple and Beats devices")
    while True:
        serial = await ainput("Enter Serial or IMEI: ")
        while True:
            solver = await get_solver()
            if solver:
                break
            await sleep(1)
        sh_checkcoverage, route, JSESSIONID, solve = solver
        await erase_captcha(JSESSIONID)
        cookies = await to_thread(get_cookies, sh_checkcoverage, route, JSESSIONID)
        data = await to_thread(generate_data, serial, solve)
        async with ClientSession(headers=headers) as session:
            resp = await session.post('https://checkcoverage.apple.com/us/en/?sn={}'.format(serial), headers=headers, cookies=cookies, data=data)
            apple_info = await to_thread(get_apple_info, await resp.read(), serial)
            for k, v in apple_info.items():
                print(f"{k}: {v}")
