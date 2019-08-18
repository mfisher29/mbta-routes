# mbta-routes

## Description
Some python code to interface with the publicly accessible MBTA API.

## Languages
Python 3.6

## Problem 1

### Instructions

To run the code for problem 1, follow the following steps:

1. clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. add owner execution permission to the shell script: `chmod 0700 run_problem_1.sh`
4. run `./run_problem_1.sh`

### Solution details

Out of the two options for the API calls,

I tried out both options and the time to receive an api response was about the same (typically between 160 - 230 ms).
So the real decision factor was whether to retrieve all the data and process it on the application end, or to rely on
the api to filter the data on the server side and return it pre-processed.

I decided to go with the filtered api call, filtering based on route types 0 and 1. I decided to go this route for the following reasons:
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

1. if not already completed, clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. add owner execution permission to the shell script: `chmod 0700 run_problem_2.sh`
4. run `./run_problem_2.sh`

### Solution details

The problem was solved by first calling the /stops endpoint for each route found in problem 1:

Api call: `https://api-v3.mbta.com/stops?fields[stop]=name&include=route&filter[route]={route_id}`

I was hoping there was a way to make just a single call to filter for all desired routes, but it appears that the api only allows for filtering by a single route at a time. So to mitigate delays due to multiple api calls (one for each route), I used the python asynchronous library, [asyncio](https://docs.python.org/3/library/asyncio.html), along with the [requests](https://2.python-requests.org/en/master/) library.

Once the data was obtained with the api calls, two dictionaries were used to house the relevant data:
1. stop_dict: a dictionary with stops as the keys and a list of routes they were on as the value. i.e. `{'Downtown Crossing': ['Red', 'Orange'], ...}`
2. stop_counts: a dictionary with routes as the keys and the count of stops along that route as the value. i.e. `{'Green-B': 24, ...}`

From here it was possible to calculate the desired outputs and display them on the command line.

## Problem 3

### Instructions

To run the code for problem 3, follow the following steps:

1. if not already completed, clone this repository: `git clone https://github.com/mfisher29/mbta-routes.git`
2. cd to mbta-routes from command line
3. add owner execution permission to the shell script: `chmod 0700 run_problem_3.sh`
4. run `./run_problem_3.sh`

### Solution details


## Testing

To run the unit tests, simply execute the following:
1. cd to mbta-routes from command line
2. add owner execution permission to the shell script: `chmod 0700 unit_test.sh`
3. run `./unit_test.sh`
