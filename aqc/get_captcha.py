from aiohttp import ClientSession
from asyncio import to_thread, sleep
from time import time

from .audio_captcha_solver import audio_captcha_solver
from .captcha_db import update_captcha
from .get_cookies import get_cookies
from .headers import headers


# formats 'image', 'audio'
def get_format(captchaMode: str='audio') -> str:
    return 'gc?t={}&timestamp={}0'.format(captchaMode, str(round(time(), 2)).replace('.', ''))


async def get_captcha(sh_checkcoverage: str, route: str, JSESSIONID: str):
    cookies = await to_thread(get_cookies, sh_checkcoverage, route, JSESSIONID)
    async with ClientSession(headers=headers) as session:
        while True:
            resp = await session.get(f'https://checkcoverage.apple.com/{await to_thread(get_format)}', headers=headers, cookies=cookies)
            captcha = await resp.json()
            if captcha['error']:
                await sleep(1)
                continue
            break
        await update_captcha(JSESSIONID, await audio_captcha_solver(captcha['binaryValue']))
        del cookies, resp, captcha
