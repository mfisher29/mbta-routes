cp ./requirements.txt ./problem_3/
cp ./logger.py ./problem_3/
cp ./config.py ./problem_3/
cp ./problem_1/get_subway_routes.py ./problem_3
cp ./problem_2/get_subway_stop_data.py ./problem_3

cd problem_3
REQ='requirements.txt'
pip3 install -r $REQ -t ./

python3 problem_3.py

rm requirements.txt
rm logger.py
rm config.py
rm get_subway_routes.py
rm get_subway_stop_data.py