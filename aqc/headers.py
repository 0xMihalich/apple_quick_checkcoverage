from .useragent import useragent


headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.8,ru-RU;q=0.5,ru;q=0.3",
            "Connection": "keep-alive",
            "Referer": "https://checkcoverage.apple.com/us/en/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            'User-Agent': useragent,
            "X-Requested-With": "XMLHttpRequest"
            }
