'''
Job for archiving bookings that are older than today
'''

from Schedule.models import Booking, Archive
def archive_bookings():
    print("Archiving started")
    from django.utils import timezone
    from django.db import transaction
        
    old_bookings = Booking.objects.filter(current_day__lt=timezone.now())
    archives_removed = 0
    
    if old_bookings.exists():
        with transaction.atomic():
            for booking in old_bookings:
                Archive.objects.create(
                    users = booking.users,
                    users_amount = booking.users_amount,
                    start_hour = booking.start_hour,
                    end_hour = booking.end_hour,
                    current_day = booking.current_day,
                )
                booking.delete()
                archives_removed += 1
        
        print(f"Archived {archives_removed} bookings.")
        
    else:
        print("Nothing to archive")


'''
Obsolete due to the use of Heroku Scheduler on prod
'''

# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.background import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# import apscheduler as aps
# from django.conf import settings
# from Schedule.models import Booking, Archive

# logger = logging.getLogger(__name__)
# scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)   
# scheduler2 = BlockingScheduler(timezone=settings.TIME_ZONE)
# def archive_bookings():
#     print("Archiving started")
#     from django.utils import timezone
#     from django.db import transaction
        
#     old_bookings = Booking.objects.filter(current_day__lt=timezone.now())
    
#     if old_bookings.exists():
#         with transaction.atomic():
#             for booking in old_bookings:
#                 Archive.objects.create(
#                     users = booking.users,
#                     users_amount = booking.users_amount,
#                     start_hour = booking.start_hour,
#                     end_hour = booking.end_hour,
#                     current_day = booking.current_day,
#                 )
#                 booking.delete()
        
#         print("scheduler shutdown - ")
#         scheduler.remove_all_jobs()
#         scheduler.shutdown()
        
#     else:
#         print("nothing to archive")
#         scheduler.remove_all_jobs()
#         scheduler.shutdown()
    
# def schedule():
#     #test to work
#     trigger = CronTrigger(
#         year = "*",
#         month = "*",
#         day = "*",
#         hour = "01",
#         minute = "00",
#         second = "00",
#     )
#     scheduler.add_job(
#         archive_bookings,
#         trigger = trigger,
#         id = "1",
#         name = "archiver",
#         replace_existing=True,
#         max_instances=1,
#         )

    
        
    # scheduler.start()
    # scheduler.start()


'''
Job for rolling a new user from the pool for cleaning duty in the current week
'''
from django.contrib.auth.models import User
from Schedule.models import CleaningSchedule, CleaningScheduleArchive
from random import choice
from datetime import date, timedelta
def cleaning_user_roll():
    # get all users that are not superuser
    all_users = [user['username'] for user in User.objects.exclude(username='Super').values()]
    
    # get all the users usernames from CleaningSchedule that were already picked in this set
    
    picked_users = [user['username'] for user in CleaningSchedule.objects.all().values()]
    
    
    # check if all the users already have been picked
    if len(all_users) == len(picked_users):
        print("all users already picked")
        user_to_archive = CleaningSchedule.objects.filter(username=picked_users[-1])[0]
        
        CleaningScheduleArchive.objects.create(
            username = user_to_archive.username,
            period_start = user_to_archive.period_start,
            period_end = user_to_archive.period_end,
        )
        
        CleaningSchedule.objects.all().delete()
        
        # adding this to prevent the last picked user from the previous set to be picked instatly again since random tends to do this way too often
        user_last_picked_last_set = [CleaningScheduleArchive.objects.all().order_by('-id')[0].username]
        # now the recent picks are empty so roll a new user
        this_weeks_user = choice(list(set(all_users)-set(user_last_picked_last_set)))
    else:
        # if there are more than 1 users in the recent picks, archive the most recent one before creating a new cleaning schedule entry
        if len(picked_users) > 0:
            user_to_archive = CleaningSchedule.objects.filter(username=picked_users[-1])[0]

            CleaningScheduleArchive.objects.create(
                username = user_to_archive.username,
                period_start = user_to_archive.period_start,
                period_end = user_to_archive.period_end,
            )
        
        # roll a new user
        this_weeks_user = choice(list(set(all_users)-set(picked_users)))
        print("this week user after roll = ", this_weeks_user)
        
        print("check picked users = ", picked_users)
        # # check if user was already picked
        # if this_weeks_user in picked_users:
        #     print("This weeks user is in picked_users")
        #     # keep rolling until new user is picked
        #     while this_weeks_user in picked_users:
                
        #         this_weeks_user = choice(all_users)
        #         print("picked user after new roll in loop = ", this_weeks_user)

    CleaningSchedule.objects.create(
        username = this_weeks_user,
        period_start = date.today(),
        period_end = date.today()+timedelta(days=7),
    )