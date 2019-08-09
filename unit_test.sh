#!/usr/bin/env bash

cp ./requirements.txt ./unit_tests/
cd unit_tests

export environment=dev
export logLevel='DEBUG'
export api_base_url=''

REQ='requirements.txt'
pip3 install -r $REQ

python3 -m unittest discover

rm requirements.txt