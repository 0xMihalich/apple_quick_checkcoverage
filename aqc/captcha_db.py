from aiosqlite import connect
from asyncio import to_thread
from typing import Optional, Tuple

from .get_timestamp import get_timestamp


captcha_base = 'aqc_base/captcha.db'
default_table = '''CREATE TABLE IF NOT EXISTS captcha (
                    sh_checkcoverage TEXT,
                    route TEXT,
                    JSESSIONID TEXT,
                    solve TEXT,
                    timestamp INTEGER,
                    UNIQUE(sh_checkcoverage)
                    );'''


def generator_tuple(answer: tuple) -> Tuple[Optional[int], ...]:
    return tuple(value[0] for value in answer if value)


async def sql_quere(quere: str=default_table, values: tuple=None):
    async with connect(captcha_base) as db:
        await db.execute(quere, values)
        await db.commit()


async def sql_fetchone(quere: str) -> tuple:
    async with connect(captcha_base) as db:
        cursor = await db.execute(quere)
        result = await cursor.fetchone()
        await cursor.close()
    return result


async def sql_fetchall(quere: str) -> tuple:
    async with connect(captcha_base) as db:
        cursor = await db.execute(quere)
        result = await cursor.fetchall()
        await cursor.close()
    return result


async def add_checkcoverage(sh_checkcoverage: str, route: str, JSESSIONID: str):
    await sql_quere('''INSERT OR IGNORE INTO captcha(sh_checkcoverage, route, JSESSIONID, timestamp)
                        VALUES(?, ?, ?, ?);''', (sh_checkcoverage, route, JSESSIONID, await get_timestamp() - 900))


async def update_captcha(JSESSIONID: str, solve: str):
    await sql_quere("UPDATE captcha SET solve = ?, timestamp = ? WHERE JSESSIONID = ?;",
                                                            (solve, await get_timestamp(), JSESSIONID))


async def erase_captcha(JSESSIONID: str):
    await sql_quere("UPDATE captcha SET timestamp = ? WHERE JSESSIONID = ?;",
                                                            (await get_timestamp() - 900, JSESSIONID))


async def return_old_solver() -> Optional[Tuple[str, ...]]:
    return await sql_fetchone(f"""SELECT sh_checkcoverage, route, JSESSIONID
                                    FROM captcha
                                    WHERE timestamp < {await get_timestamp()-890};""")


async def get_solver() -> Optional[Tuple[str, ...]]:
    return await sql_fetchone(f"""SELECT sh_checkcoverage, route, JSESSIONID, solve
                                    FROM captcha
                                    WHERE timestamp >= {await get_timestamp()-890}
                                    ORDER BY RANDOM()
                                    LIMIT 1;""")


async def get_timestamps() -> Tuple[Optional[int], ...]:
    return await to_thread(generator_tuple, await sql_fetchall("SELECT timestamp FROM captcha;"))


async def get_count() -> int:
    (count, ) = await sql_fetchone("SELECT count(sh_checkcoverage) FROM captcha;")
    return count
