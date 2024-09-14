from django.contrib import admin
from .models import Booking, Archive
import logging
from django.http import HttpResponse
from django.contrib import messages


from django.urls import path
from django.shortcuts import render, redirect

# Register your models here.
logger = logging.getLogger(__name__)

@admin.action(description="Zarchiwizuj rezerwacje starsze niz dzisiejsze")
def archive_bookings(modeladmin, request, queryset):
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

class MyAdminSite(admin.AdminSite):
    site_header = "Panel Admina"
    index_template = "admin/admin_panel.html"
    
    def archive_action(self, request):
        if request.method == "GET":
            self.archive_function(request)
        
        return redirect('/admin')
    
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('archive_action/', self.admin_view(self.archive_action), name='archive_action'),
        ]

        return custom_urls + urls
     
    def keycode_function(self, request):
        import random
        NEW_CODE = [random.randint(0,9) for i in range(4)]
        THIS_MONTH_CODE = ""
        for item in NEW_CODE:
            THIS_MONTH_CODE += str(item)
            
        THIS_MONTH_CODE = int(THIS_MONTH_CODE) 
        return THIS_MONTH_CODE
        
    def archive_function(self, request):
        print("TEST")
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
            messages.info(request, "Zarchiwizowano dane pomyslnie")
        else:
            messages.warning(request, "Nie ma danych do archiwizacji")
            
admin_site = MyAdminSite(name='admin_panel')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    ordering = ['current_day']
    list_display=('id','users','users_amount','start_hour','end_hour','current_day')
    search_fields=('users','current_day')
    list_filter=('current_day','users')
    actions=[archive_bookings]


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    ordering = ['current_day']
    list_display=('id','users','users_amount','start_hour','end_hour','current_day')
    search_fields=('users','current_day')
    list_filter=('users','start_hour','current_day')     