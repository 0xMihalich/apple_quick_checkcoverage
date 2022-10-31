from aiosqlite import connect
from asyncio import to_thread

from .get_captcha_blocks import get_captcha_blocks


async def audio_captcha_solver(captcha: str) -> str:
    async with connect('aqc_base/audio_captcha.db') as db:
        cursor = await db.execute("SELECT captcha, audio FROM audio_captcha")
        audio_captcha = await cursor.fetchall()
    return "".join(captcha for block in await to_thread(get_captcha_blocks, captcha)
                                    for captcha, audio in audio_captcha if audio in block)
