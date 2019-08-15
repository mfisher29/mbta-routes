import logger
from utils import get_stops_api_call
from get_subway_routes import get_subway_routes
import time

logger = logger.get_logger()


def get_subway_stop_data(route_list):
    start = time.time()

    # create dict with keys from results of problem 1, initiate to 0 counts
    stop_dict = dict.fromkeys(route_list, 0)

    for route in route_list:
        response = get_stops_api_call(route)
        # need to handle error (400 level) cases
        stop_dict[route] = len(response['data'])

    # part 1: route with most stops & number of stops
    max_stops_route = max(stop_dict, key=stop_dict.get)
    logger.info(f"Route with most stops: {max_stops_route}, Stops: {stop_dict[max_stops_route]}")

    # part 2: route with least stops & number of stops
    min_stops_route = min(stop_dict, key=stop_dict.get)
    logger.info(f"Route with least stops: {min_stops_route}, Stops: {stop_dict[min_stops_route]}")

    # part 3: list of connecting stops and route names for those stops

    end = time.time()
    logger.info(f"Total program time: {'%.5f'%(end-start)} (s)")


get_subway_stop_data(get_subway_routes()[1])
