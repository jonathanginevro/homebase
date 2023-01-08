# Homebase :baseball:

Homebase is a baseball web application that showcases standings and statistics for MLB teams and players. To run this program, please refer to the setup steps listed below. Alternatively, there are instructions at the bottom for a startup stript that executes all steps.

### Setup Steps

Firstly, the following must be installed to setup the virtual environment and run the application. This includes pipenv, Django, requests, lxml and beautifulsoup4. This can be done using the following:
```bash
pip install pipenv
pip install Django
pip install requests
pip install lxml
pip install beautifulsoup4
```
We must then initialize our virtual environment and databse. This can be down via the following commands:
```bash
python3 -m virtualenv venv
source venv/bin/activate
./homebase/manage.py migrate
```

Lastly, to run the server, execute the following:
```bash
./homebase/manage.py runserver
```

### Setup Script
This entire process is included in the `start.sh` script. To run the script, execute the following:
```bash
source ./start.sh
```
