from django.apps import AppConfig

class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Schedule'
    
    #Functionality for APScheduler (obsolete on Heroku prod)
    #Starts the scheduler after loading the projects conf
    
    # def ready(self):
    #     from . import jobs
    #     jobs.schedule()

    