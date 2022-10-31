from asyncio import sleep

from .captcha_db import return_old_solver
from .get_captcha import get_captcha


# бесконечный скрипт обновления капч
async def update_captchas():
    while True:
        old_solver = await return_old_solver()
        if old_solver:
            sh_checkcoverage, route, JSESSIONID = old_solver
            await get_captcha(sh_checkcoverage, route, JSESSIONID)
            continue
        await sleep(0.1)