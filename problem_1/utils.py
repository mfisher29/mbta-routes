import requests
import logger
from config import API_URL_BASE
import time

logger = logger.get_logger()


def get_routes_api_call(filters):
    start = time.time()
    try:
        resp = requests.get(url=f'{API_URL_BASE}?filter[type]={filters}')
        finish = time.time()
        logger.info(f"API response received after {'%.5f'%(finish - start)} seconds.")
        return resp.json()

    except requests.exceptions.ConnectionError:
        logger.exception(requests.exceptions.RequestException)
        finish = time.time()
        logger.error(f"API connection refused after {'%.5f'%(finish - start)} seconds.")
        return None


def process_response(r):
    output = ''
    if r:
        try:
            for route in r['data']:
                output = output + route['attributes']['long_name'] + ', '
            return output[:-2]  # cut off final space and comma for clean output
        except KeyError:
            return f'KeyError when processing json response: {r}'
    else:
        return 'No response body to process'
