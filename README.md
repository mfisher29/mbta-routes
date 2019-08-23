# mbta-routes

## Description
Some python code to interface with the publicly accessible MBTA API.

## Dependencies
Python 3.6 - or [latest release](https://www.python.org/downloads/)

## Problem 1

### Instructions

To run the code for problem 1, follow the following steps:

For Unix (MAC) machines:
1. clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. add owner execution permission to the shell script: `chmod 0700 run_problem_1.sh`
4. run `./run_problem_1.sh`

For non-Unix machines:
1. clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. run:
```
cp ./logger.py ./problem_1/
cp ./config.py ./problem_1/
```
4. run `cd problem_1`
5. run `pip3 install requests`
6. run `python3 problem_1.py`
7. run:
```
rm logger.py
rm config.py
```

### Solution details

I tried out both options and the time to receive an api response was about the same (typically between 160 - 230 ms).
So the real decision factor was whether to retrieve all the data and process it on the application end, or to rely on
the api to filter the data on the server side and return it pre-processed.

I decided to go with the filtered api call, filtering based on route types 0 and 1:
`https://api-v3.mbta.com/routes?include=stop&filter[type]=0,1`

I decided to go this route for the following reasons:
- less data stored in memory: the json response will always be smaller in this case than calling the api without the filters. Holding less data in memory is better.
- simplicity: with the filtered api call, it's clear what data the code is looking for and this is easier for a new developer to read and understand
- modularity: by inputting the filters via a config file, the code can be changed easily to filter for other route types
- scalability: in the un-filtered case, the amount of data returned could become very large at any time if the MBTA adds more data to their system.
So even though the run times are similar now, if the returned response gets much larger, processing time on the client side will have a larger increase with the un-filtered call
- easier to test: can unit test with fake small json blocks rather than having to try to mock out the larger response which could be quite varied
- less prone to bugs: less data coming back so less room for potential decoding/parsing errors

## Problem 2

### Instructions

To run the code for problem 2, follow the following steps:

For Unix (MAC) machines:
1. if not already completed, clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. add owner execution permission to the shell script: `chmod 0700 run_problem_2.sh`
4. run `./run_problem_2.sh`

For non-Unix machines:
1. if not already completed, clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. run:
```
cp ./logger.py ./problem_2/
cp ./config.py ./problem_2/
cp ./problem_1/get_subway_routes.py ./problem_2
```
4. run `cd problem_2`
5. run `pip3 install requests`
6. run `python3 problem_2.py`
7. run:
```
rm logger.py
rm config.py
rm get_subway_routes.py
```

You will notice problem 1 also runs upon executing the shell script. This is because problem 2 builds on 1, using the outputs generated from problem 1.

### Solution details

The problem was solved by first calling the /stops endpoint for each route found in problem 1:

Api call: `https://api-v3.mbta.com/stops?fields[stop]=name&include=route&filter[route]={route_id}`

I was hoping there was a way to make just a single call to filter for all desired routes, but it appears that the api only allows for filtering by a single route at a time. So to mitigate delays due to multiple api calls (one for each route), I used the python asynchronous library, [asyncio](https://docs.python.org/3/library/asyncio.html), along with the [requests](https://2.python-requests.org/en/master/) library.

Once the data was obtained with the api calls, two dictionaries were used to house the relevant data:
1. stop_dict: a dictionary with stops as the keys and a list of routes they were on as the value. i.e. `{'Downtown Crossing': ['Red', 'Orange'], ...}`
2. stop_counts_dict: a dictionary with routes as the keys and the count of stops along that route as the value. i.e. `{'Green-B': 24, ...}`

From here it was possible to calculate the desired outputs and display them on the command line.

## Problem 3

### Instructions

To run the code for problem 3, follow the following steps:

For Unix (MAC) machines:
1. if not already completed, clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. add owner execution permission to the shell script: `chmod 0700 run_problem_3.sh`
4. run `./run_problem_3.sh`

For non-Unix machines:
1. if not already completed, clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. run:
```
cp ./logger.py ./problem_3/
cp ./config.py ./problem_3/
cp ./problem_1/get_subway_routes.py ./problem_3
cp ./problem_2/get_subway_stop_data.py ./problem_3
```
4. run `cd problem_3`
5. run `pip3 install requests`
6. run `python3 problem_3.py`
7. run:
```
rm logger.py
rm config.py
rm get_subway_routes.py
rm get_subway_stop_data.py
```

You will notice problems 1 and 2 also run upon executing the shell script. This is because problem 3 builds on 1 and 2, using the outputs generated from problems 1 and 2.

### Solution details

There is probably an easier way to retrieve route stops and recommended trips though the API, like the stop longitude and latitudes that are available. However in this case I wanted to try to solve it based on the data I already had collected from the API calls in problems 1 and 2. 

The key part of the code is the `check_connections` function, which handles cases where a rider must transfer between 1 or more routes to get to their end stop. It first finds a potential connecting stop from the connecting_stops dictionary from problem 2:
`{'Park Street': ['Red', 'Green-C', ...], 'State': ['Orange', 'Blue'], ... }`
It then looks to see if the end stop is along any of the listed routes. If YES, a response is returned. If NO, the sequence is repeated to check for another connection, until we finally find a connecting stop that will allow us to get to the desired route which has our final destination stop.

The code is structured to perform the following sequential tasks:
- Handle case sensitivity and validate input
- Checks for simple case where start and end stop are along the same route, if YES, response is returned - if NO, continue through code
- Call the check_connections function and append all possible routes to a list
- Determines the shortest route out of the available options. If routes are equivalent the first route in the list is chosen, response is returned

Currently the algorithm handles up to 2 subway transfers. To allow it to handle N subway transfers, this
algorithm could be improved upon by turning check_connections into a recursive function. The way it is solved now is a bit messy but shows my stream of thoughts. It also fails for the case where you need to transfer more than twice (i.e. Mattapan --> Bowdoin where you need to transfer between Mattapan, Red, Orange/Green, and Blue).


## Testing

### unit tests

To run the unit tests, simply execute the following:

For Unix (MAC) machines:
1. cd to mbta-routes from command line
2. add owner execution permission to the shell script: `chmod 0700 unit_test.sh`
3. run `./unit_test.sh`

For non-Unix machines:
1. cd to mbta-routes from command line
2. run:
```
cp ./logger.py ./unit_tests
cp ./config.py ./unit_tests
```
3. run `cd unit_tests`
4. run `pip3 install requests`
5. run `python3 -m unittest discover`
6. run:
```
rm logger.py
rm config.py
```

### integration tests

To run the integration tests, simply execute the following:

For Unix (MAC) machines:
1. cd to mbta-routes from command line
2. add owner execution permission to the shell script: `chmod 0700 integration_test.sh`
3. run `./integration_test.sh`

For non-Unix machines:
1. cd to mbta-routes from command line
2. run:
```
cp ./logger.py ./integration_tests
cp ./config.py ./integration_tests
cp ./problem_1/get_subway_routes.py ./integration_tests
cp ./problem_2/get_subway_stop_data.py ./integration_tests
```
3. run `cd integration_tests`
4. run `pip3 install requests`
5. run `python3 -m unittest discover
6. run `python3 test_route_planner.py`
7. run:
```
rm logger.py
rm config.py
rm get_subway_routes.py
rm get_subway_stop_data.py
```

** Note: the integration tests have sleeps inserted to prevent rate-limiting errors. They will take a couple minutes to run.
