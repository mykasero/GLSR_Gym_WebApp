web: gunicorn GLSR_Gym.wsgi
release: ./manage.py collectstatic --noinput
release: ./manage.py migrate --no-input
release: ./manage.py loaddata template_data.json