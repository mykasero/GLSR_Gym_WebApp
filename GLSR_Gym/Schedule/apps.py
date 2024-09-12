from django.apps import AppConfig
# from django.contrib.admin import apps

# class MyAdminConfig(apps.AdminConfig):
#     default_site="Schedule.admin.MyAdminSite"
#     # label = 'custom-admin'
class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Schedule'
