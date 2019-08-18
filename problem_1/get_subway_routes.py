from config import API_URL_BASE, FILTERS
import requests
import logger
import time

logger = logger.get_logger()


def get_subway_routes():
    start = time.time()
    filter_str = ''
    # populate string of route filter values to use in the api call
    for f in FILTERS:
        filter_str = f'{filter_str}{f},'
    response = get_routes_api_call(filter_str[:-1])
    if response.status_code == 200:
        json_resp = response.json()
        outputs = process_response(json_resp)
        logger.info(f'Route long names: {outputs[0]}')
    else:
        logger.error(f"API call failed with code={response.status_code}: {response.text}")
        # using .text on the response in case the error response body is not json
        outputs = ['', []]  # empty since there is no route data to process
    end = time.time()
    logger.info(f"Total run time for problem 1: {'%.5f'%(end-start)} (s)\n")
    return outputs


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
