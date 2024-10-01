from django.core.management.base import BaseCommand
from Schedule.models import Archive
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "<Command for remove archived bookings older than 1m in order to preserve memory>"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Looking for old archives that can be removed")
        self.rows_deleted = 0
        removable_archives = Archive.objects.filter(current_day__lt=(timezone.now()-timedelta(days=30)))
        
        if removable_archives.exists():
            self.stdout.write("Found some old archives ready for removal")
            for record in removable_archives:
                record.delete()
                self.rows_deleted += 1
            self.stdout.write(f"Old archives ({self.rows_deleted}) removed successfully")            
            
        else:
            self.stdout.write("No data found ready for removal")

        

            