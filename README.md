# Homebase :baseball:

Homebase is a baseball web application that showcases standings and statistics for MLB teams and players. To run this program, refer to the startup steps listed below. Alternatively, there are instructions at the bottom for a startup stript that executes all steps.

### Startup Steps

Firstly, to setup the virtual environment, install pipenv and make the following initializations:
```bash
pip install pipenv
python3 -m virtualenv venv
source venv/bin/activate
```
There are other installiations that need to be made in the virtual environment. This includes Django, requests, lxml and beautifulsoup4. This can be done by running the following:
```bash
pip install Django
pip install requests
pip install lxml
pip install beautifulsoup4
```
Lastly, to initialize the database and run the server, execute the following:
```bash
./homebase/manage.py migrate
./homebase/manage.py runserver
```

### Startup Script
This entire process is included in the `start.sh` script. Execute the following to run the script:
```bash
source ./start.sh
```
