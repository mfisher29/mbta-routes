#!/usr/bin/env bash

cp ./logger.py ./problem_1/
cp ./config.py ./problem_1/

REQ='requirements.txt'
pip3 install -r $REQ

cd problem_1
python3 problem_1.py

rm logger.py
rm config.py