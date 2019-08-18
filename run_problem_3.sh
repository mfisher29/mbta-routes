#!/usr/bin/env bash

cp ./requirements.txt ./problem_3/
cp ./logger.py ./problem_3/
cp ./config.py ./problem_3/
cp ./utils.py ./problem_3/
cp ./problem_1/get_subway_routes.py ./problem_3
cd problem_3
REQ='requirements.txt'
pip3 install -r $REQ -t ./

python3 route_planner.py

rm requirements.txt
rm logger.py
rm config.py
rm utils.py
rm get_subway_routes.py