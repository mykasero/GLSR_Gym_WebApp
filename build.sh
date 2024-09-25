#!/usr/bin/env bash

#Req install

pip install -r requirements.txt

#collectstatic
python manage.py collectstatic --no-input

#make migrations
python manage.py makemigrations

#migrate
python manage.py migrate

#loaddata
# python manage.py loaddata template_data.json


#migrate
# python manage.py migrate