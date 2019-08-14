#!/usr/bin/env bash

export environment='qa'
export logLevel='DEBUG'
export api_base_url=''

if [ "${environment}" == 'prod' ]; then
    echo "Not executing integration_tests in prod!"
    exit 0
fi

cd integration_tests
REQ='requirements.txt'
pip3 install -r $REQ -t ./

# api test
python3 test_display_resubmit_api.py