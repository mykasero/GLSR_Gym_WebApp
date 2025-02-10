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

# function for calculating how many days user booked this year
def yearly_counter(user_name):
    yearly_days_total = 0
    
    for month_total in month_attendance_counter(user_name).values():
        yearly_days_total += month_total
        
    return yearly_days_total
# function for calculating how many days user booked this month
def this_month_activity(user_name):
    this_month_total = 0
    month_num = [1,2,3,4,5,6,7,8,9,10,11,12]
    current_month = datetime.now().month
    
    for month_days, month_num in zip(month_attendance_counter(user_name).items(),month_num):
        if month_num == current_month:
            this_month_total = month_days[1]
        
    return this_month_total

# function for getting the current month name
def current_month_name(month_number):
    month_names = ["Styczeń", "Luty", "Marzec",
              "Kwiecień", "Maj", "Czerwiec",
              "Lipiec","Sierpień", "Wrzesień",
              "Październik", "Listopad", "Grudzień"]
    
    return month_names[month_number-1]

# return one of 6 ranks, named from tierI to tierVI
def monthly_rank(user_name):
    this_month_amount = this_month_activity(user_name)
    lower_req = [0,2,5,6,8,12]
    upper_req = [2,5,6,8,10,32]
    tiers = ["I","II","III","IV","V","VI"]
    names = ["Crossfitowiec", "Chudzielec", "Człowiek Szczupły (obelga)",
             "Szczur Bojowy", "Wielki Chłop", "Ogromny Chłop",]
    
    '''
        ~30 Days in a month, let's take avg of 3 days per week which gives 12 (4weeks * 3) total days so:
        <2 attendance - rank 1
        2 - 5 - rank 2
        5 - 6 - rank 3
        6 - 8 - rank 4
        8 - 10 - rank 5
        >12 - rank 6 (max rank)
    '''
    for lower,upper, tier, name in zip(lower_req,upper_req, tiers, names):
        if lower <= this_month_amount < upper:
            return ["TIER " + tier, name]
        
        
# return one of 10 ranks, named from tierI to tierX
def yearly_rank(user_name):
    
    total_activity = yearly_counter(user_name)
    lower_req = [0,10,25,40,55,70,85,100,130,150]
    upper_req = [10,25,40,55,70,85,100,130,150,367]
    tiers = ["I","II","III","IV","V","VI","VII","VIII","IX","X"]
    names = ["Świeżak", "Crossfitowiec", "Chudy Szczur", "Chudzielec", "Człowiek Szczupły (obelga)",
             "Wyszczurzony", "Szczur Bojowy", "Duży Chłop", "Wielki Chłop", "Ogromny Chłop",]
    
    '''
        ~365 Days in a year, let's take avg of 3 days per week which gives 156 (52weeks * 3) total days so:
        <10 attendance - rank 1
        10 - 25 - rank 2
        25 - 40 - rank 3
        40 - 55 - rank 4
        55 - 70 - rank 5
        70 - 85 - rank 6
        85 - 100 - rank 7
        100 - 130 - rank 8
        130 - 150 - rank 9
        >150 - rank 10 (max rank)
        
    '''
    for lower,upper, tier, name in zip(lower_req,upper_req, tiers, names):
        if lower <= total_activity < upper:
            return ["TIER " + tier, name]
    
def next_month():
    '''
        Function for calculating the next month (7th day) to use it in the users payment expiry_date
    '''
    today = datetime.today()
    
    if today.month == 12:
        next_month = today.replace(year=today.year+1, month=1,day=7)
    else:
        next_month = today.replace(month=today.month+1, day=7)
        
    return next_month.strftime('%Y-%m-%d')

def check_last_payment(user_payments_info):
    '''
        Function to check if the last expiry of the payment was over 2months,
        so the users account can be deactivated (not deleted!)
    '''
    user_payments_info = user_payments_info
    expiry_dates = [item.expiry_date for item in user_payments_info]
    current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'),'%Y-%m-%d').date()
    expired_accs = []
    
    if len(list(user_payments_info)) == len(expiry_dates):
        for expiry_date, user_record in zip(expiry_dates, user_payments_info):
            if expiry_date != None:
                if (current_date-expiry_date).total_seconds()/(60*60*24) > 60:
                    expired_accs.append('+')
                else:
                    expired_accs.append('---')
            else:
                expired_accs.append("NONE")        
            
    for user_record, expired_account in zip(user_payments_info, expired_accs):
        user_record.is_expired = expired_account
    
    return user_payments_info

def reset_is_paid(user_list):
    user_list = user_list
    
    for users_info in user_list:
        if users_info.is_paid == True and datetime.today().date() > users_info.expiry_date:
            users_info.is_paid = False
            users_info.save()