from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "<Command for running a job that archives booking entries older than 1d>"
    def handle(self, *args, **kwargs):
        from Schedule.jobs import archive_bookings
        self.stdout.write("Starting archiver job")
        archive_bookings()
        self.stdout.write("Ended archiver job")