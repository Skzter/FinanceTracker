# Finance Tracker
Simple Finance Tracker which you can host yourself. It uses
Django on the Backend with Bootstrap 5 in the Frontend. 

## Setup 
At first clone the Repo and make a new Python Virtual Environment.
```
git clone https://github.com/Skzter/FinanceTracker.git
cd FinanceTracker
python3 -m venv ~/path/to/venv
source ~/path/to/venv/bin/activate
```
You can check if your virtual environment uses the correct python with `which python`.
It should return `your/home/path/to/env/bin/python`.
Now install Django with Pip.
```
pip install django
```
If everything worked you should be able to run `python manage.py runserver` without any issues.
If thats the case press "CTRL+C" to exit and run `python data.py` to populate the database with some test data.
Now you run `python manage.py runserver` and everything should run smoothly. Visit the adress given by 
django in your browser and you will see the finance tracker and can play around with it.
