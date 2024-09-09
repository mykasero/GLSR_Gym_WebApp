from django.contrib import admin
from models import Booking, Archive
# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=('id','users','users_amount','start_hour','end_hour','current_day')
    search_fields=('users','current_day')
    list_filter=('users','start_hour','current_day')

@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display=('id','users','users_amount','start_hour','end_hour','current_day')
    search_fields=('users','current_day')
    list_filter=('users','start_hour','current_day')     