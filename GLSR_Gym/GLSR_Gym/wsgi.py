"""
WSGI config for GLSR_Gym project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GLSR_Gym.GLSR_Gym.settings')
#pre-render
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GLSR_Gym.settings')


application = get_wsgi_application()
