from django.contrib import admin
from django.urls import path
from . import views

app_name = "Schedule"

urlpatterns = [
    path("", views.home, name = "home"),
    path('login/', views.login, name = "login"),
    path('login/success/', views.login_success, name = "login_success"),
    path('register/', views.register, name = "register"),
    path('lobby/', views.lobby, name = "lobby"),
    path('booking/', views.booking, name = "booking"),
    path('archive/', views.archive_booking, name = "archive"),
    path('admin/', admin.site.urls),
]