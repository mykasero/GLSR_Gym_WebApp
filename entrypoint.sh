#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "POSTGRES STARTED"
fi

#python manage.py flush --no-input
#python manage.py migrate


#Collect static
echo "Collect static"
python manage.py collectstatic --noinput
#Apply migrations
echo "Apply db migrations"
python manage.py migrate
#Populate dbs with template data
echo "Populating DBs"
python manage.py loaddata template_data.json
#Apply migrations
echo "Apply db migrations"
python manage.py migrate

#Create sample superuser
if [ "#DJANGO_SUPERUSER_USERNAME " ]
then
    echo "Creating Superuser"
    python manage.py createsuperuser \
    --no-input \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL 

fi


exec "$@"

