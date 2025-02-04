from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Payment
from Schedule.admin import admin_site

# profiles list shown in admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user","email","date_joined"]
    fields = ["user","email","date_joined","profile_picture"]

# payments list shown in admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user","is_paid","payment_date","expiry_date"]
    field = ["user","is_paid","payment_date","expiry_date"]

# register profiles if they don't exist already in the admin profiles list
if Profile not in admin_site._registry:
    admin_site.register(Profile, ProfileAdmin)
    
# register payments if they don't exist already in the admin payments list
    
if Payment not in admin_site._registry:
    admin_site.register(Payment, PaymentAdmin)