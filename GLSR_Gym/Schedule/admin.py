from django.contrib import admin
from .models import Booking, Archive
import logging

admin.site.index_template = 'admin/admin_panel.html'

from django.urls import path
from django.shortcuts import render

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
#### working on the button stuff
# in admin_panel.html <a href="{% url 'Schedule:archive_action' %}" class="nice_buttons">Archiwizuj dane</a>
# from django.utils.html import format_html
# from django.contrib import messages
# from django.http import HttpResponseRedirect

# class MyAdminSite(admin.AdminSite):
#     site_header = "custom_admin"
    
#     def archive_action(self, request):
#         print("HERE #@!#!@#!@#!@")
#         self.archive_function()
#         self.message_user(request, "Action successful")
        
#         return HttpResponseRedirect("/admin/")
    
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('archive_action/', self.admin_view(self.archive_action), name='archive_action')
#         ]
#         return custom_urls + urls
    
#     def archive_function(self):
#         from django.utils import timezone
#         from django.db import transaction
            
#         old_bookings = Booking.objects.filter(current_day__lt=timezone.now())
        
#         if old_bookings.exists():
#             with transaction.atomic():
#                 for booking in old_bookings:
#                     Archive.objects.create(
#                         users = booking.users,
#                         users_amount = booking.users_amount,
#                         start_hour = booking.start_hour,
#                         end_hour = booking.end_hour,
#                         current_day = booking.current_day,
#                     )
#                     booking.delete()
#             logger.info("Success")
#         else:
#             logger.info("No rows to archive")

# admin_site = MyAdminSite(name='custom_admin')


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