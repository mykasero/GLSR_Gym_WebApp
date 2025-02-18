from django.contrib import admin
from .models import Booking, Archive, Keycodes, BugReports, CleaningSchedule
import logging
from django.http import HttpResponse
from django.contrib import messages
from .forms import KeycodeForm
from django.utils import timezone
from datetime import timedelta

from django.urls import path
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect

from sys import stdout



# Custom action for archiving bookings older than today
@admin.action(description="Zarchiwizuj rezerwacje starsze niz dzisiejsze")
def archive_bookings(modeladmin, request, queryset):
    from django.utils import timezone
    from django.db import transaction
        
    # Get all bookings older than today    
    old_bookings = Booking.objects.filter(current_day__lt=timezone.now())
    
    # If there are such bookings, loop through them and copy + add the records to the Archive table
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
                # Remove booking from current bookings table
                booking.delete()
                
        messages.info(request, "Zarchiwizowano dane pomyslnie")
    else:
        messages.warning(request, "Nie ma danych do archiwizacji")


#Custom Admin 
class MyAdminSite(admin.AdminSite):
    site_header = "Panel Admina"
    
    #base site URL
    index_template = "admin/admin_panel.html"
    
    # Check user permission
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff
    
    # Archive bookings view
    def archive_action(self, request):
        if not self.has_permission(request):
            return self.login(request)
        
        context = self.each_context(request)
        
        # If sent method is POST, start the archive function and redirect to admin base URL
        if request.method == "POST":
            self.archive_function(request)
            return redirect('/admin')
        # If sent method is GET, render the template and forms/buttons etc
        else:
            return render(request, 'admin/archive_action.html', context)
            
    
    # View for changing keycodes to the key stash
    def new_keycode(self, request):
        # Create new form
        form = KeycodeForm()
        # form = KeycodeForm(request.POST)
        
        # Get context
        context = self.each_context(request)
        # Add the form to the context
        context.update({
            'form' : form,
        })
        
        if request.method == "POST":
            # Get Form 
            form = KeycodeForm(request.POST)
            
            if form.is_valid():
                # If the new keycode is not the same as the last 10 keycodes then save the new code
                if self.not_last_ten(form.cleaned_data['code']) == True:
                    form.save() 
                    print(form)
                    messages.info(request,f"Pomyslnie dodano nowy kod: {form.cleaned_data['code']}")
                    return redirect('/admin')
                # If the new keycode is the same as one of the last 10 keycodes, throw a message to the user
                else:
                    messages.error(request,"Kod ostatnio uzywany, podaj inny kod")  
                    return render(request, 'admin/new_keycode.html', context)
        else:
            form = KeycodeForm()
            return render(request, 'admin/new_keycode.html', context)
    
    # View for cleaning the archive from records older than 1 month
    def clean_archive(self, request):      
        context = self.each_context(request)
        
        # If the method is POST, start the removing function and after that redirect to admin base URL
        if request.method == "POST":
            self.remove_archives(request)
            
            return redirect('/admin')
        # If the method is GET, render the template and forms/buttons etc
        else:
            
            return render(request, 'admin/clean_archive.html', context)
    
    # Add custom urls for the new views            
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('archive_action/', self.admin_view(self.archive_action), name='archive_action'),
            path('new_keycode/', self.admin_view(self.new_keycode), name='new_keycode'),
            path('clean_archive/', self.admin_view(self.clean_archive), name='clean_archive'),
        ]

        return custom_urls + urls
     
    # Function for archiving bookings older than today
    def archive_function(self, request):
        from django.utils import timezone
        from django.db import transaction
        
        # Get all bookings older than today    
        old_bookings = Booking.objects.filter(current_day__lt=timezone.now())
        
        # If there are such bookings, loop through them and copy + add the records to the Archive table
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
                    # Remove booking from current bookings table
                    booking.delete()
                    
            messages.info(request, "Zarchiwizowano dane pomyslnie")
        else:
            messages.warning(request, "Nie ma danych do archiwizacji")
    
    # Function for checking if the new keycode has already been used in the last 10 codes        
    def not_last_ten(self, code):
        code = code
        # Get the list of codes sorted by the newest to oldest
        code_list = list(Keycodes.objects.all().order_by('-id').values_list('code'))
        
        # if there are more than 10 codes, get only 10 newest ones
        if len(code_list) > 10:
            LAST_CODES = [code_list[i][0] for i in range(10)]
        # if there are less than 10 codes, get all of them
        else:
            LAST_CODES = [code_list[i][0] for i in range(len(code_list))]
        
        # If the new code is has not been used already return True
        if code not in LAST_CODES:
            return True
        # IF the new code has been already used return False
        else:
            return False
    
    # Function for removing archive records older than 1 month
    def remove_archives(self, request):
        self.rows_deleted = 0
        # Get all archive records older than 1 month
        removable_archives = Archive.objects.filter(current_day__lt=(timezone.now()-timedelta(days=30)))
        
        # If there are any such records, loop over them and delete each one + count how many got deleted
        if removable_archives.exists():
            for record in removable_archives:
                record.delete()
                self.rows_deleted += 1
            messages.info(request, f"Usunięto pomyślnie {self.rows_deleted} starych wpisów")        
            
        else:
            messages.warning(request, "Nie ma żadnych wystarczająco starych wpisów do usunięcia")

      
admin_site = MyAdminSite(name='admin_panel')

# Create a Booking model in admin panel
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    ordering = ['current_day']
    list_display=('id','users','users_amount','start_hour','end_hour','current_day', 'created_by')
    search_fields=('users','current_day')
    list_filter=('current_day','users')
    actions=[archive_bookings]

# Create an Archive model in admin panel
@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    ordering = ['current_day']
    list_display=('id','users','users_amount','start_hour','end_hour','current_day')
    search_fields=('users','current_day')
    list_filter=('users','start_hour','current_day')     
   
# Create a Keycode model in admin panel    
@admin.register(Keycodes)
class KeycodeAdmin(admin.ModelAdmin):
    ordering = ['-code_date']
    list_display=('id','code','code_date')

# Create a BugReport model in admin panel    
@admin.register(BugReports)
class BugReportAdmin(admin.ModelAdmin):
    ordering = ['-report_date']
    list_display=('id','report_text','report_date')
    
# Create a CleaningSchedule model in admin panel    
@admin.register(CleaningSchedule)
class CleaningScheduleAdmin(admin.ModelAdmin):
    ordering = ['-period_start']
    list_display=('username','period_start','period_end')