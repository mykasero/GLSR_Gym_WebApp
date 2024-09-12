from django.contrib import admin
from .models import Booking, Archive
import logging
from django.http import HttpResponse
admin.site.index_template = 'admin/admin_panel.html'


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
#### working on the button stuff
# in admin_panel.html <a href="{% url 'Schedule:archive_action' %}" class="nice_buttons">Archiwizuj dane</a>
from django.utils.html import format_html
from django.contrib import messages
from django.http import HttpResponseRedirect

class MyAdminSite(admin.AdminSite):
    site_header = "Panel Admina"
    index_template = "admin/admin_panel.html"
    # def get_app_list(self, request, **kwargs):
    #     """Show some links in the admin UI.

    #     See also https://stackoverflow.com/a/56476261"""
    #     app_list = super().get_app_list(request, kwargs)
    #     app_list += [
    #         {
    #             "name": "Other actions",
    #             "app_label": "other_actions_app",
    #             "models": [
    #                 {
    #                     "name": "my name",
    #                     "object_name": "my object name'custom_admin:archive_function'",
    #                     "view_only": True,
    #                 }
    #             ],
    #         },
    #     ]
    #     return app_list

    def archive_action(self, request):
        print("HERE #@!#!@#!@#!@")
        # self.archive_function()
        print(request.method)
        print(request)
        if request.method == "POST":
            print("button works")
        
        return redirect('/admin/archive_action')
    
    def get_urls(self):
        # self.app_index_template = 'admin/admin_panel.html'
        urls = super().get_urls()
        # print("URLS - HERE")
        custom_urls = [
            path('archive_action/', self.admin_view(self.archive_action), name='archive_action'),
        ]
        # print("URLS2 - HERE", custom_urls+urls)

        return custom_urls + urls
     
    

    def archive_function(self):
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
            logger.info("Success")
        else:
            logger.info("No rows to archive")
            
    

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