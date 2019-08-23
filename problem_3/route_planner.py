import logger
from get_subway_stop_data import get_subway_stop_data
from get_subway_routes import get_subway_routes

logger = logger.get_logger()


def route_planner(start, end):
    # handle case sensitivity
    start = start.lower()
    end = end.lower()

    # passing in route list from problem 1 to get_subway_stop_data from problem 2 in order to retrieve needed data
    response = get_subway_routes()
    if response is not None:
        routes = response[1]
        [stop_dict, connecting_stop_dict] = get_subway_stop_data(routes)
    else:
        return 'Leading API call failed, wait and try again.'

    # convert all dict keys to lower case to remove case sensitivity of input
    stop_dict = dict((k.lower(), v) for k, v in stop_dict.items())
    connecting_stop_dict = dict((k.lower(), v) for k, v in connecting_stop_dict.items())

    # validate inputs, ensure they are actually valid subway stops
    if start in stop_dict and end in stop_dict:

        # first check for simple case where stops are on the same route
        for route in stop_dict[start]:
            if route in stop_dict[end]:
                return f'Answer: {start.capitalize()} --> {end.capitalize()}: {route}'

        # if no value is returned will proceed to this case:
        # determine route for stop, check for connecting stops along that line
        # check if final stop is on the other route

        # if starting point only has 1 route, we know we need to look for connections along that route
        if len(stop_dict[start]) == 1:
            route_ls = []
            curr_route = stop_dict[start][0]
            route_ls = check_connections(stop_dict, connecting_stop_dict, start, end, curr_route, route_ls, False)
            print(f'ROUTE LIST: {route_ls}')
            route_str = ', '.join(route_ls)
            return f'Answer: {start.capitalize()} --> {end.capitalize()}: {route_str}'

        # need to handle connection cases where the starting point has more than 1 possible route
        else:
            # find all potential routes, return the shortest one
            potential_routes = []
            for route in stop_dict[start]:
                rt_list = []

                # add route list to list of potential routes (list of lists)
                # find route list with fewest elements, that is the optimal answer
                potential_routes.append(check_connections(stop_dict, connecting_stop_dict, start, end, route, rt_list, False))
                logger.debug(f'List of potential routes: {potential_routes}')

            # find minimum length route list (least transfers), initiate with first choice from potential routes
            shortest_rt = potential_routes[0]
            for rail_route in potential_routes:
                if len(rail_route) < len(shortest_rt):
                    shortest_rt = rail_route

            route_str = ', '.join(shortest_rt)
            return f'Answer: {start.capitalize()} --> {end.capitalize()}: {route_str}'
    else:
        return f'Invalid subway stops: {start.capitalize()}, {end.capitalize()}'


def check_connections(stop_dict, connection_dict, start_stop, end_stop, current_route, route_list, check_additional_connections):
    # list of routes that the ending stop is on
    end_routes = stop_dict[end_stop]

    for connection_stop_1 in connection_dict:
        if connection_stop_1 == start_stop:
            continue  # pass over case of first connection and start stop, don't want to go backwards

        # check if connecting stop is along original route
        if current_route in connection_dict[connection_stop_1]:
            logger.debug(f'2. Found a potential connection: {connection_stop_1}')
            # now look along the other stops in the dict for another connection

            for route in connection_dict[connection_stop_1]:
                if route == current_route:
                    # pass over case of equivalent route, we don't need to check along same route
                    continue
                elif route in end_routes:
                    route_list.append(current_route)
                    route_list.append(route)
                    return route_list
                else:
                    if check_additional_connections:
                        current_route = route
                        # find connecting stops along this new route
                        for connection_stop_2 in connection_dict:
                            if connection_stop_1 == connection_stop_2 or connection_stop_2 == start_stop:
                                continue  # pass over case of first connection and start stop, don't want to go backwards

                            if current_route in connection_dict[connection_stop_2]:
                                logger.debug(f'3. Found a potential connection: {connection_stop_2}')

                                for r in end_routes:  # in case there is more than 1 end route
                                    # check if end route (r) is in the list of routes for the connecting stop
                                    if r in connection_dict[connection_stop_2]:
                                        route_list.append(current_route)
                                        route_list.append(route)
                                        route_list.append(r)
                                        return route_list
                                    else:
                                        # end route is not in list of connecting stop routes, continue
                                        continue
                            else:
                                # looped through potential connection routes and didn't find a match, continue
                                continue
                    else:
                        # want to loop through all potential connections before moving on
                        continue
        else:
            continue

    # went through each stop in the connection dict and didn't find a possible connection to link the two stops
    # check for additional connections, start over since we don't want to miss stops that we already looped through
    check_additional_connections = True
    check_connections(stop_dict, connection_dict, start_stop, end_stop, current_route, route_list, check_additional_connections)
