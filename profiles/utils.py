from django.contrib.auth.models import User
from profiles.models import Profile
from Schedule.models import Archive, Booking
from datetime import datetime

def month_attendance_counter(user_name):
    '''
        Function for splitting booked days into a list with month : amount of days format.
        Ex.: [{'April':15,'May':9}]
    '''
    
    all_user_rows = Archive.objects.filter(users=user_name).values()
    
    months = {"Styczeń":0, "Luty":0, "Marzec":0,
              "Kwiecień":0, "Maj":0, "Czerwiec":0,
              "Lipiec":0,"Sierpień":0, "Wrzesień":0,
              "Październik":0, "Listopad": 0, "Grudzień":0}
    month_num = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    
    for month_name, month_number in zip(months.keys(),month_num):
        ctr = 0
        for row_data in all_user_rows:
            if row_data['current_day'].strftime("%-m") == str(month_number) and row_data['current_day'].strftime("%Y") == datetime.now().strftime("%Y"):
                ctr+=1
                
        months[month_name] = ctr
        ctr = 0
    
    return months

def yearly_counter(user_name):
    yearly_days_total = 0
    
    for month_total in month_attendance_counter(user_name).values():
        yearly_days_total += month_total
        
    return yearly_days_total

def this_month_activity(user_name):
    this_month_total = 0
    month_num = [1,2,3,4,5,6,7,8,9,10,11,12]
    current_month = datetime.now().month
    
    for month_days, month_num in zip(month_attendance_counter(user_name).items(),month_num):
        print(f"month - {month_days[0]}, days - {month_days[1]}, curr_month - {current_month} days - {month_num}")
        if month_num == current_month:
            this_month_total = month_days[1]
        
    return this_month_total

def current_month_name(month_number):
    month_names = ["Styczeń", "Luty", "Marzec",
              "Kwiecień", "Maj", "Czerwiec",
              "Lipiec","Sierpień", "Wrzesień",
              "Październik", "Listopad", "Grudzień"]
    
    return month_names[month_number-1]