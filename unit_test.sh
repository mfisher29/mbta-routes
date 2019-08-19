#!/usr/bin/env bash

cp ./logger.py ./unit_tests/
cp ./config.py ./unit_tests/

export environment=dev
export logLevel='DEBUG'
export api_base_url=''

REQ='requirements.txt'
pip3 install -r $REQ

cd unit_tests
python3 -m unittest discover

rm logger.py
rm config.py