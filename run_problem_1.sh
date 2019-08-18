cp ./requirements.txt ./problem_1/
cp ./logger.py ./problem_1/
cp ./config.py ./problem_1/
cd problem_1
REQ='requirements.txt'
pip3 install -r $REQ -t ./

python3 problem_1.py

rm requirements.txt
rm logger.py
rm config.py