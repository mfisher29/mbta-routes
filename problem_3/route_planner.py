import logger
from get_subway_stop_data import get_subway_stop_data
from get_subway_routes import get_subway_routes
import random

logger = logger.get_logger()


def route_planner(start, end):
    # validate inputs, ensure they are actually valid subway stops
    # handle case sensitivity
    print(start, end)

    [stop_dict, connecting_stop_dict] = get_subway_stop_data(get_subway_routes()[1])
    print(stop_dict)

    if start in stop_dict and end in stop_dict:
        print('\nvalid route! calculating...')

        # first check for simple case where stops are on the same route
        for route in stop_dict[start]:
            if route in stop_dict[end]:
                return f'{start} --> {end}: {route}'

        # if no value is returned will proceed to this case:
        # determine route for stop, check for connecting stops along that line
        # check if final stop is on the other route

        # if starting point only has 1 route, we know we need to look for connections along that route
        if len(stop_dict[start]) == 1:
            route_ls = []
            curr_route = stop_dict[start][0]
            print(f'\ncurrent route: {curr_route}')

            route_ls = check_connections(stop_dict, connecting_stop_dict, start, end, curr_route, route_ls)
            print(f'route list output: {route_ls}')
            route_str = ', '.join(route_ls)
            return f'answer: {start} --> {end}: {route_str}'

        # need to handle connection cases where the starting point has more than 1 possible route
        else:
            # find all potential routes, return the shortest one
            potential_routes = []
            for route in stop_dict[start]:
                rt_list = []

                # add route list to list of potential routes (list of lists)
                # find route list with fewest elements, that is the optimal answer
                potential_routes.append(check_connections(stop_dict, connecting_stop_dict, start, end, route, rt_list))
                print(potential_routes)

            # find minimum length route list (least transfers)
            # initiate with random choice from potential routes
            # this could be improved by checking the longitudes and latitudes with another api call, or altering the
            # current api call, to find stops that are at the shortest distances between each other
            # for now, just deciding based on least # of stops. If equal # of stops, the decision will be random
            shortest_rt = random.choice(potential_routes)
            for rail_route in potential_routes:
                if len(rail_route) < len(shortest_rt):
                    shortest_rt = rail_route

            route_str = ', '.join(shortest_rt)
            return f'answer: {start} --> {end}: {route_str}'


def check_connections(stop_dict, connection_dict, start_stop, end_stop, current_route, route_list):
    for stop in connection_dict:
        # check if the starting route is in the list of routes for the connecting stop
        if current_route in connection_dict[stop]:
            logger.info(f'1. found a potential connection: {stop}')
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
    print('no direct connection, looking for additional transfer...')

    end_routes = stop_dict[end_stop]

    for connection_stop_1 in connection_dict:
        # check if the starting route is in the list of routes for the connecting stop
        current_route = stop_dict[start_stop][0]
        # check if connecting stop is along original route
        if current_route in connection_dict[connection_stop_1]:
            print(f'2. found a potential connection: {connection_stop_1}')
            # now look along the other stops in the dict for another connection

            for route in connection_dict[connection_stop_1]:
                print(current_route, route)
                if route == current_route:
                    # pass over case of equivalent route, already determined we don't need to check along same route
                    continue
                else:
                    # find connecting stops along this new route
                    for connection_stop_2 in connection_dict:
                        if connection_stop_1 == connection_stop_2 or connection_stop_2 == start_stop:
                            continue  # pass over case of first connection and start stop, don't want to go backwards
                        for r in end_routes:  # in case there is more than 1 end route
                            # check if end route (r) is in the list of routes for the connecting stop
                            if r in connection_dict[connection_stop_2]:
                                print(f'connecting stop 2: {connection_stop_2}')
                                route_list.append(current_route)
                                route_list.append(route)
                                route_list.append(r)
                                return route_list
                            else:
                                # end route is not in list of connecting stop routes, continue
                                continue
                        # looped through potential end routes and didn't find a match, continue
                        continue


starting_stop = input("Please enter starting point station: ")
ending_stop = input("Please enter your final destination: ")
print(route_planner(starting_stop, ending_stop))
