#!/usr/bin/env bash

cp ./requirements.txt ./problem_1/
cd problem_1
REQ='requirements.txt'
pip3 install -r $REQ -t ./

python3 get_subway_routes.py