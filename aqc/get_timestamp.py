from asyncio import to_thread
from time import time


async def get_timestamp() -> int:
    return int(await to_thread(time))
