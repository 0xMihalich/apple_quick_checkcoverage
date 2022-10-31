from asyncio import sleep

from .captcha_db import get_count
from .get_sh_checkcoverage import get_sh_checkcoverage


# скрипт создания базы капч
async def create_captcha_db():
    while True:
        count = await get_count()
        if count < 3:
            await get_sh_checkcoverage()
            continue
        break
    del count