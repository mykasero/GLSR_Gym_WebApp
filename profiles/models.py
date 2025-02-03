from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(db_column="Adres Email",default="twoj_email@gmail.com")
    date_joined = models.DateTimeField(db_column="Data dołączenia",default="2024-09-01") 
    profile_picture = models.ImageField(db_column="Zdjęcie profilowe",upload_to='media/pfps/',default='media/pfps/blank_user.png')
    
    def __str__(self):
        return self.user.username

# Model for checking the users payment for the monthly access
class Payment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null = True, blank = True)
    expiry_date = models.DateField(null=True, blank = True)
     

# Create User Profile on User account registration + Create blank payment record
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Creates profiles for already registered users
        Profile.objects.create(user=instance, date_joined = instance.date_joined)
        # Creates payment record for already registered users
        Payment.objects.create(user=instance)
    else:
        # Creates profile for newly registered user
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.date_joined = instance.date_joined
        profile.save()
        
        # Creates payment record for newly registered user
        payment, _ = Payment.objects.get_or_create(user=instance)
        payment.save()
        
        
