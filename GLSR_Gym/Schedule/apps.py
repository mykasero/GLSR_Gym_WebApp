from django.apps import AppConfig

class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Schedule'
    
    def ready(self):
        from . import jobs
        jobs.schedule()

#Needs more research
# def Keybox_code():
#     #code for the box with the key to the gym
#     from datetime import date
#     import random
    
#     THIS_MONTH_CODE = None 
    
#     if date.today().day == 1:
#         NEW_CODE = [random.randint(0,9) for i in range(4)]
#         THIS_MONTH_CODE = ""
#         for item in NEW_CODE:
#             THIS_MONTH_CODE += str(item)
            
#         THIS_MONTH_CODE = int(THIS_MONTH_CODE)
#         OLD_CODE = THIS_MONTH_CODE
#         return THIS_MONTH_CODE
#     else:
#         return OLD_CODE
        
    