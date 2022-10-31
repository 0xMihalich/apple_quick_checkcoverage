def get_cookies(sh_checkcoverage: str, route: str, JSESSIONID: str) -> dict:
    return {
            'sh_checkcoverage': sh_checkcoverage,
            'route': route,
            'JSESSIONID': JSESSIONID,
            'POD': 'us~en',
            'CC_AFFINITY': 'awsapse1-2'
            }
