source env/bin/activate
pip install -r requirements.txt
screen -S ${PWD##/} -dm python bot.py
