#!/bin/bash

pip install pipenv
python3 -m virtualenv venv
source venv/bin/activate
pip install Django
pip install requests
pip install lxml
pip install beautifulsoup4
./homebase/manage.py migrate
./homebase/manage.py runserver