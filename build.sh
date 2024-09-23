#!/usr/bin/env bash

#Exit on error
set - o errexit

#Req install

pip install -r requirements.txt

#collectstatic
python manage.py collectstatic --no-input

#migrate
python manage.py migrate

#loaddata
python manage.py loaddata template_data.json

#migrate
python manage.py migrate