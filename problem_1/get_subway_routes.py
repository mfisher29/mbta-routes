import logger
from config import FILTERS
from utils import get_routes_api_call, process_response
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
