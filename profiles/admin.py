from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile
from Schedule.admin import admin_site

# profiles list shown in admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user","email","date_joined"]
    fields = ["user","email","date_joined","profile_picture"]

# register profiles if they don't exist already in the admin profiles list
if Profile not in admin_site._registry:
    admin_site.register(Profile, ProfileAdmin)
    
