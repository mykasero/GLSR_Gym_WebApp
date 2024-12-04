def month_attendance_counter(user_name):
    '''
        Function for splitting booked days into a list with month : amount of days format.
        Ex.: [{'April':15,'May':9}]
    '''
    from django.contrib.auth.models import User
    from profiles.models import Profile
    from Schedule.models import Archive, Booking
    from datetime import datetime
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