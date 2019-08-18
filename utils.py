import requests
import logger
from config import API_URL_BASE
import time

logger = logger.get_logger()


# utils for problem 1

def get_routes_api_call(filters):
    start = time.time()
    try:
        resp = requests.get(url=f'{API_URL_BASE}routes?filter[type]={filters}')
        finish = time.time()
        logger.debug(f"API response received after {'%.5f'%(finish - start)} seconds.")
        return resp

    except requests.exceptions.ConnectionError:
        logger.exception(requests.exceptions.RequestException)
        finish = time.time()
        logger.error(f"API connection refused after {'%.5f'%(finish - start)} seconds.")
        return None


def process_response(r):
    output_str = ''
    output_list = []
    if r:
        try:
            for route in r['data']:
                long_name = route['attributes']['long_name']
                route_id = route['id']
                output_list.append(route_id)
                output_str = output_str + long_name + ', '
            # return value is a list containing the string of routes to display and a list of routes
            # [:-2] is to cut off final space and comma for clean output
            return [output_str[:-2], output_list]
        except KeyError:
            return f'KeyError when processing json response: {r}'
    else:
        return 'No response body to process'


# utils for problem 2
