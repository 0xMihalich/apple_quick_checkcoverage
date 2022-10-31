from base64 import decodebytes
from typing import Tuple


def get_captcha_blocks(captcha: str) -> Tuple[bytes, ...]:
    cut = b'\x80'
    return *(solve.strip(cut) for solve in decodebytes(captcha.encode())[64044:].split(cut*37872) if len(solve.strip(cut)) > 15990),
