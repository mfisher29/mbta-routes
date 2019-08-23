import logger
from get_subway_stop_data import get_subway_stop_data
from get_subway_routes import get_subway_routes

logger = logger.get_logger()


def route_planner(start, end):
    start = start.lower()
    end = end.lower()

    # calling fxns from problems 1 & 2 to generate a dict of all stops and a dict of all connecting stops
    response = get_subway_routes()
    if response is not None:
        all_routes_list = response[1]
        [stop_dict, connecting_stop_dict] = get_subway_stop_data(all_routes_list)
    else:
        return 'Leading API call failed, wait and try again.'

    # convert all dict keys to lower case to remove case sensitivity of input
    stop_dict = dict((k.lower(), v) for k, v in stop_dict.items())
    connecting_stop_dict = dict((k.lower(), v) for k, v in connecting_stop_dict.items())

    # validate inputs, ensure they are actually valid subway stop names
    if start in stop_dict and end in stop_dict:

        # first check for simple case where stops are on the same route
        for route in stop_dict[start]:
            if route in stop_dict[end]:
                return f'Answer: {start.capitalize()} --> {end.capitalize()}: {route}'

        # if no value is returned will proceed to find all potential connecting routes
        potential_routes = []
        for route in stop_dict[start]:
            # add route list to list of potential routes (list of lists)
            potential_routes.append(check_connections(stop_dict, connecting_stop_dict, start, end, route))
            logger.debug(f'List of potential routes: {potential_routes}')

        # find shortest route (least transfers), initiate with first choice from potential routes
        shortest_route = potential_routes[0]
        for rail_route in potential_routes:
            if len(rail_route) < len(shortest_route):
                shortest_route = rail_route

        route_str = ', '.join(shortest_route)
        return f'Answer: {start.capitalize()} --> {end.capitalize()}: {route_str}'
    else:
        return f'Invalid subway stops: {start.capitalize()}, {end.capitalize()}'


def check_connections(stop_dict, connection_dict, start_stop, end_stop, current_route):
    route_list = []
    for stop in connection_dict:
        # check if the starting route is in the list of routes for the connecting stop
        if current_route in connection_dict[stop]:
            logger.debug(f'1. Found a potential connection: {stop}')
            # look along the other route(s) in the list for the end stop
            for route in connection_dict[stop]:
                if route == current_route:
                    # pass over case of equivalent route, already determined we don't need to check along same route
                    continue
                else:
                    if route in stop_dict[end_stop]:
                        route_list.append(current_route)
                        route_list.append(route)
                        return route_list

    # went through each stop in the connection dict and didn't find a possible connection to link the two stops
    # check for secondary connection, start over since we don't want to miss stops that we already looped through
    logger.debug('No direct connection, looking for additional transfer...')

    for connection_stop_1 in connection_dict:
        # set current route to route that starting stop is on
        current_route = stop_dict[start_stop][0]
        # check if connecting stop is along original route
        if current_route in connection_dict[connection_stop_1]:
            logger.debug(f'2. Found a potential connection: {connection_stop_1}')
            # now look along the other stops in the dict for another connection

            for route in connection_dict[connection_stop_1]:
                if route == current_route:
                    # pass over case of equivalent route, already determined we don't need to check along same route
                    continue
                else:
                    # find connecting stops along this new route
                    for connection_stop_2 in connection_dict:
                        if connection_stop_1 == connection_stop_2 or connection_stop_2 == start_stop:
                            continue  # pass over case of first connection and start stop, don't want to go backwards

                        for r in stop_dict[end_stop]:  # in case there is more than 1 end route
                            # check if end route (r) is in the list of routes for the connecting stop
                            if r in connection_dict[connection_stop_2]:
                                route_list.append(current_route)
                                route_list.append(route)
                                route_list.append(r)
                                return route_list
                            else:
                                # end route is not in list of connecting stop routes, continue
                                continue
