import logger
from config import FILTERS
from utils import get_routes_api_call, process_response
import time

logger = logger.get_logger()


def get_subway_routes():
    start = time.time()
    filter_str = ''
    for f in FILTERS:
        filter_str = f'{filter_str}{f},'
    response = get_routes_api_call(filter_str[:-1])
    final_output = process_response(response)
    if final_output:
        logger.info(final_output)
    end = time.time()
    logger.info(f"Total program time: {'%.5f'%(end-start)} (s)")


get_subway_routes()
