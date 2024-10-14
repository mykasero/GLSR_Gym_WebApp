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
