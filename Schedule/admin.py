from django.contrib import admin
from .models import Booking, Archive, Keycodes
import logging
from django.http import HttpResponse
from django.contrib import messages
from .forms import KeycodeForm

from django.urls import path
from django.template.response import TemplateResponse
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
    def has_permission(self,request):
        user = request.user
        return user.is_staff and user.is_active
    
    def archive_action(self, request):
        if request.method == "POST":
            self.archive_function(request)
            return redirect('/admin')
        
        return TemplateResponse(request, 'admin/archive_action.html', self.each_context(request))
    
    def new_keycode(self, request):
        
        form = KeycodeForm(request.POST)
        context = self.each_context(request)
        context.update({
            'form' : form,
        })
        if request.method == "POST":
            print("here")
            if form.is_valid():
                if self.not_last_ten(form.cleaned_data['code']) == True:
                    form.save() 
                    print(form)
                    messages.info(request,f"Pomyslnie dodano nowy kod: {form.cleaned_data['code']}")
                    return redirect('/admin')
                else:
                    messages.error(request,"Kod ostatnio uzywany, podaj inny kod")  
                    return render(request, 'admin/new_keycode.html', context)
        else:
            return render(request, 'admin/new_keycode.html', context)
                
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('archive_action/', self.admin_view(self.archive_action), name='archive_action'),
            path('new_keycode/', self.admin_view(self.new_keycode), name='new_keycode'),
        ]

        return custom_urls + urls
     
        
    def archive_function(self, request):
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
            
    def not_last_ten(self, code):
        code = code
        code_list = list(Keycodes.objects.all().order_by('-id').values_list('code'))
        
        if len(code_list) > 10:
            #take ten last used codes to avoid posting the same one
            LAST_CODES = [code_list[i][0] for i in range(10)]
        else:
            LAST_CODES = [code_list[i][0] for i in range(len(code_list))]
        
        print(f"TEST KOD {code}  ----- {LAST_CODES}")
        
        if code not in LAST_CODES:
            return True
        else:
            return False
        
        
            
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