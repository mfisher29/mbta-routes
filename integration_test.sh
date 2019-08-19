#!/usr/bin/env bash

export environment='qa'
# don't have qa endpoints for the api so will run against actual endpt

cp ./logger.py ./integration_tests/
cp ./config.py ./integration_tests/
cp ./problem_1/get_subway_routes.py ./integration_tests/
cp ./problem_2/get_subway_stop_data.py ./integration_tests/

if [ "${environment}" == 'prod' ]; then
    echo "Not executing integration_tests in prod!"
    exit 0
fi

REQ='requirements.txt'
pip3 install -r $REQ

cd integration_tests
python3 -m unittest discover
python3 test_route_planner.py

rm logger.py
rm config.py
rm get_subway_routes.py
rm get_subway_stop_data.py