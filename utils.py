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
        logger.info(f"API response received after {'%.5f'%(finish - start)} seconds.")
        return resp.json()

    except requests.exceptions.ConnectionError:
        logger.exception(requests.exceptions.RequestException)
        finish = time.time()
        logger.error(f"API connection refused after {'%.5f'%(finish - start)} seconds.")
        return None


def process_response(r):
    output = ''
    output_list = []
    if r:
        try:
            for route in r['data']:
                long_name = route['attributes']['long_name']
                route_id = route['id']
                output_list.append(route_id)
                output = output + long_name + ', '
            return [output[:-2], output_list]  # cut off final space and comma for clean output, return route id list
        except KeyError:
            return f'KeyError when processing json response: {r}'
    else:
        return 'No response body to process'


# utils for problem 2

def get_stops_api_call(route):
    start = time.time()
    try:
        resp = requests.get(url=f'{API_URL_BASE}stops?include=route&filter[route]={route}')
        finish = time.time()
        logger.info(f"API response received after {'%.5f'%(finish - start)} seconds.")
        return resp.json()

    except requests.exceptions.ConnectionError:
        logger.exception(requests.exceptions.RequestException)
        finish = time.time()
        logger.error(f"API connection refused after {'%.5f'%(finish - start)} seconds.")
        return None
