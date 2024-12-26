from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile_home, name='profile_home'),
    path('profile/activity-chart/', views.profile_activity_chart, name='activity-chart'),
    path('profile/email/<int:pk>/edit/', views.edit_email, name='edit_email'),
    path('profile/pfp/<int:pk>/edit/', views.edit_pfp, name='edit_pfp'),
    path('profile/rank_info', views.rank_info, name='rank_info'),
]