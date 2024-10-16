from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .admin import admin_site
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name = "home"),
    path("home/", views.home, name = "home"),
    path('login/', views.login, name = "login"),
    path('login/login_success/', views.login_success, name = "login_success"),
    path('logout/', views.logout, name = "logout"),
    path('register/', views.register, name = "register"),
    path('lobby/', views.lobby, name = "lobby"),
    path('booking/', views.booking, name = "booking"),
    path('current_bookings/' , views.current_bookings, name="current_bookings"),
    path('archive/', views.archive_booking, name = "archive"),
    path('bug_report/', views.bug_report, name="bug_report"),
    path('reports/', views.reports, name = "reports"),
    path('gallery/', views.gallery, name = "gallery"),
]