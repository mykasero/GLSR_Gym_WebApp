"""
ASGI config for GLSR_Gym project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

#render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GLSR_Gym_Proj.GLSR_Gym.settings')

#pre render
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GLSR_Gym.settings')

application = get_asgi_application()
