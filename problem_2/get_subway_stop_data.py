from config import API_URL_BASE
import requests
import asyncio
import logger
import time

logger = logger.get_logger()


def get_subway_stop_data(route_list):
    start = time.time()
    if route_list is None:
        logger.warning('No input given')
        return None
    stop_dict = {}
    stop_counts_dict = {}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_subway_stops_api_calls(loop, route_list, stop_dict, stop_counts_dict))

    # if there is no data in the dict, that means the api calls failed, so exit program
    # could implement some retry logic here with a short sleep to prevent 429 error again
    if stop_counts_dict == {}:
        return None

    # part 1 and 2: find max and min stops
    max_min_dict = get_max_min_stops(stop_counts_dict)
    logger.info(f"Route with most stops: {max_min_dict['max']}, Stops: {stop_counts_dict[max_min_dict['max']]}")
    logger.info(f"Route with least stops: {max_min_dict['min']}, Stops: {stop_counts_dict[max_min_dict['min']]}")

    # part 3: display stops that connect two or more subway routes and the route names
    connecting_stops_dict = get_connecting_stops(stop_dict)
    logger.info(f"Connecting stops: {connecting_stops_dict}")

    end = time.time()
    logger.info(f"Total run time for problem 2: {'%.5f'%(end-start)} (s)\n")

    return [stop_dict, connecting_stops_dict]


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
            if json_resp['data']:
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
                logger.error(f'No json data to read, possible bad request: {routes}')
                return None
        else:
            logger.error(f'API call failed with code {response.status_code} : {response.text}')
            return None  # data won't be accurate if an error is thrown for a given api call, so exiting call loop


def get_max_min_stops(stop_counts):
    # part 1: route with most stops & number of stops
    max_stops_route = max(stop_counts, key=stop_counts.get)

    # part 2: route with least stops & number of stops
    min_stops_route = min(stop_counts, key=stop_counts.get)

    return {'max': max_stops_route, 'min': min_stops_route}


def get_connecting_stops(stops):
    connecting_stops = {}
    for stop in stops:
        if len(stops[stop]) > 1:
            connecting_stops[stop] = stops[stop]
    return connecting_stops

