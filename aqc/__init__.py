from asyncio import gather, get_event_loop

from .apple_checkcoverage import apple_checkcoverage
from .captcha_db import sql_quere
from .create_captcha_db import create_captcha_db
from .update_captchas import update_captchas


def app():
    loop = get_event_loop()
    try:
        loop.run_until_complete(sql_quere())
        apps = gather(*[create_captcha_db(), update_captchas(), apple_checkcoverage()])
        loop.run_until_complete(apps)
    except KeyboardInterrupt:
        print("\nApp cancel by User.")
        apps.cancel()
        loop.run_forever()
        apps.exception()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
