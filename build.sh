#!/usr/bin/env bash

#Req install

pip install -r requirements.txt

#collectstatic
python manage.py collectstatic --no-input

#migrate
python manage.py migrate

#loaddata
python manage.py loaddata template_data.json

#make migrations
python manage.py makemigrations

#migrate
python manage.py migrate