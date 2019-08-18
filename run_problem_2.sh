cp ./requirements.txt ./problem_2/
cp ./logger.py ./problem_2/
cp ./config.py ./problem_2/
cp ./problem_1/get_subway_routes.py ./problem_2
cd problem_2
REQ='requirements.txt'
pip3 install -r $REQ -t ./

python3 problem_2.py

rm requirements.txt
rm logger.py
rm config.py
rm get_subway_routes.py