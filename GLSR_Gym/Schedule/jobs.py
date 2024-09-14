from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from django.conf import settings
from Schedule.models import Booking, Archive
import logging

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

def archive_bookings():
    from django.utils import timezone
    from django.db import transaction
        
    old_bookings = Booking.objects.filter(current_day__lt=timezone.now())
    
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
        logger.info("Success")
    else:
        logger.info("No rows to archive")
    scheduler.shutdown(wait=False)
    
def schedule():
    trigger = CronTrigger(
        year = "*",
        month = "*",
        day = "*",
        hour = "21",
        minute = "18",
        second = "0",
    )
    scheduler.add_job(
        archive_bookings,
        trigger = trigger,
        name = "archiver",
        )
    
    scheduler.start()