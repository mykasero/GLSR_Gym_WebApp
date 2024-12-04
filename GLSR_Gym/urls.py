"""
URL configuration for GLSR_Gym project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Schedule.admin import admin_site
from django.conf import settings
from django.conf.urls.static import static as static_staging

from django.templatetags.static import static
from django.views.generic.base import RedirectView

#rest test
from rest_framework import routers
from REST import views as REST_views
router = routers.DefaultRouter()
router.register(r'users', REST_views.UserViewSet)
router.register(r'groups', REST_views.GroupViewSet)



admin_site._registry.update(admin.site._registry)
urlpatterns = [
    path('', include('Schedule.urls')),
    path('', include('profiles.urls')),
    path('admin/', admin_site.urls),
    path('', include("django.contrib.auth.urls")),
    path('favicon.ico', RedirectView.as_view(url=static('favicon.ico'))),
    path('', include(router.urls)),
    path('', include('REST.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] 

if settings.DEBUG:
    urlpatterns += static_staging(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
