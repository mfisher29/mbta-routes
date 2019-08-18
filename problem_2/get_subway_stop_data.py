import logger
from get_subway_routes import get_subway_routes
from config import API_URL_BASE
import requests
import time
import asyncio

logger = logger.get_logger()


def get_subway_stop_data(route_list):
    start = time.time()
    stop_dict = {}
    stop_counts = {}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_subway_stops_api_calls(loop, route_list, stop_dict, stop_counts))

    # if there is no data in the dict, that means the api calls failed, so exit program
    # could implement some retry logic here with a short sleep to prevent 429 error again
    if stop_counts == {}:
        return None

    # part 1: route with most stops & number of stops
    max_stops_route = max(stop_counts, key=stop_counts.get)
    logger.info(f"Route with most stops: {max_stops_route}, Stops: {stop_counts[max_stops_route]}")

    # part 2: route with least stops & number of stops
    min_stops_route = min(stop_counts, key=stop_counts.get)
    logger.info(f"Route with least stops: {min_stops_route}, Stops: {stop_counts[min_stops_route]}")

    # part 3: display stops that connect two or more subway routes and the route names
    connecting_stops = {}
    for stop in stop_dict:
        if len(stop_dict[stop]) > 1:
            connecting_stops[stop] = stop_dict[stop]
    logger.info(f"Connecting stops: {connecting_stops}")

    end = time.time()
    logger.info(f"Total run time for problem 2: {'%.5f'%(end-start)} (s)\n")


async def get_subway_stops_api_calls(loop, routes, stop_dict, stop_counts):
    try:
        futures = [loop.run_in_executor(None, requests.get,
                   f'{API_URL_BASE}stops?fields[stop]=name&include=route&filter[route]={r}')
                   for r in routes]
    except requests.exceptions.ConnectionError:
        logger.error(requests.exceptions.RequestException)
        return None
    for response in await asyncio.gather(*futures):
        if response.status_code == 200:
            json_resp = response.json()
            route = json_resp['data'][0]['relationships']['route']['data']['id']  # just need 1st element to get route
            stop_counts[route] = len(json_resp['data'])

            for stop in json_resp['data']:
                stop_name = stop['attributes']['name']
                if stop_name in stop_dict:
                    stop_dict[stop_name].append(route)
                else:
                    stop_dict[stop_name] = [route]
            pass
        else:
            logger.error(f'API call failed with code {response.status_code} : {response.text}')
            return None  # data won't be accurate so exiting call loop
    # return stop_dict, stop_counts if i move this to another file (i.e. utils)

# track start time here.... may need return value
get_subway_stop_data(get_subway_routes()[1])
