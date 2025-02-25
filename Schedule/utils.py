from Schedule.jobs import cleaning_user_roll
from datetime import date
from Schedule.models import CleaningSchedule
'''
Function to reroll the currently picked user
'''
def cleaning_user_reroll():
    if date.today().strftime("%A") == "Monday":
        cleaning_user_roll(True, 7, False)
    else:
        day_of_the_week = date.today().isoweekday()
        days_until_monday = (8-day_of_the_week)%7
        cleaning_user_roll(True, days_until_monday, False)
    
'''
    Function to clean the CleaningSchedule table manually, which will prevent rarely active users from being leftover in the pool and rolled constatly.
'''    
def cleaning_user_roll_cleanup():
    CleaningSchedule.objects.all().delete()