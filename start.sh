#!/bin/bash

pip install pipenv
pip install Django
pip install requests
pip install lxml
pip install beautifulsoup4
python3 -m virtualenv venv
source venv/bin/activate
./homebase/manage.py migrate
./homebase/manage.py runserver