from django.apps import AppConfig

class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GLSR_GYM_Proj.Schedule'
    
    def ready(self):
        from . import jobs
        jobs.schedule()

    