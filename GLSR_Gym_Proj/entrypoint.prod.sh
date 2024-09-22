#!/bin/sh

#render
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_URL $DB_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

#pre render
# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $DB_HOST $DB_PORT; do
#         sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi


#Collect static
echo "Collect static"
python manage.py collectstatic --noinput
#Apply migrations
echo "Apply db migrations"
python manage.py migrate
#add template sample data
echo "Populating DBs"
python manage.py loaddata template_data.json
#migrations
echo "Apply db migrations"
python manage.py makemigrations
python manage.py migrate
#Create sample superuser
# if [ "#DJANGO_SUPERUSER_USERNAME " ]
# then
#     echo "Creating Superuser"
#     python manage.py createsuperuser \
#     --no-input \
#     --username $DJANGO_SUPERUSER_USERNAME \
#     --email $DJANGO_SUPERUSER_EMAIL 
# fi


exec "$@"