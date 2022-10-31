from aiohttp import ClientSession
from asyncio import to_thread
from typing import Tuple

from .captcha_db import add_checkcoverage
from .get_captcha import get_captcha
from .useragent import useragent


def get_from_cookies(cookies: object) -> Tuple[str, ...]:
    sh_checkcoverage = cookies['sh_checkcoverage'].value
    route = cookies['route'].value
    JSESSIONID = cookies['JSESSIONID'].value
    return sh_checkcoverage, route, JSESSIONID


async def get_sh_checkcoverage():
    async with ClientSession(headers={'User-Agent': useragent}) as session:
        resp = await session.get('https://checkcoverage.apple.com/us/en/', headers={'User-Agent': useragent})
        sh_checkcoverage, route, JSESSIONID = await to_thread(get_from_cookies, resp.cookies)
        await add_checkcoverage(sh_checkcoverage, route, JSESSIONID)
        await get_captcha(sh_checkcoverage, route, JSESSIONID)
        del resp, sh_checkcoverage, route, JSESSIONID
