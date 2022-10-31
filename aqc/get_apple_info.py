from datetime import datetime, timedelta
from json import loads
from re import search, findall, compile

from .exceptions import apple_checkcoverage_error


def get_activate(endDate: str, warranty: str, model: str) -> str:
    if not endDate:
        return ''
    if warranty == 'AppleCare':
        if any(device in model.lower() for device in ('mac', 'display', 'tv')):
            days = 1095
        else:
            days = 730
    else:
        days = 365
    return str(datetime.strptime(endDate, '%Y-%m-%d').date() - timedelta(days=days))


def get_endDate(endDate: str) -> str:
    if not endDate:
        return ''
    return str(datetime.strptime(endDate, '%Y-%m-%d').date() + timedelta(days=1))


def get_snError(errorMsg: str) -> str:
    errorMsg = errorMsg.lower()
    if 'replaced' in errorMsg:
        return 'Replaced device'
    elif 'unable' in errorMsg:
        return 'Not found'
    return 'snError'


def get_Warranty(resultLabel: str) -> str:
    resultLabel = resultLabel.lower()
    if 'validated' in resultLabel:
        return 'Not Validate'
    elif 'activate' in resultLabel:
        return 'Not Activated'
    elif 'active' in resultLabel:
        return 'In Warranty'
    elif 'applecare' in resultLabel:
        return 'AppleCare'
    elif 'expired' in resultLabel:
        return 'Out of Warranty'
    return 'Unknown'


def get_apple_info(page_content: bytes, serial: str) -> dict:
    # структура
    result = {
    'serial': serial.upper(),
    'model': '',
    'warranty': '',
    'activate': '',
    'endDate': ''
    }
    xml = page_content.decode()
    errors = dict(findall(compile('(error.*?): "(.*?)",'), xml))
    if errors['errorType'] == 'captchaError':
        raise apple_checkcoverage_error('captcha error')
    elif errors['errorType'] == 'snError':
        result['warranty']=get_snError(errors['errorMsg'])
    elif not errors['errorType']:
        info = loads(search(r'responseJson",({".+)\)', xml).group(1))
        productInfo = info['productInfo']
        results = info['results'][-1]
        result['serial'] = productInfo['SERIAL_ID']
        result['model'] = productInfo['PROD_DESCR']
        result['warranty'] = get_Warranty(results['resultLabel'])
        result['endDate'] = get_endDate(results['endDate'])
        result['activate'] = get_activate(result['endDate'], result['warranty'], result['model'])
        del info, productInfo
    del errors
    return result
    
    