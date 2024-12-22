from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(db_column="Adres Email",default="twoj_email@gmail.com")
    date_joined = models.DateTimeField(db_column="Data dołączenia",default="2024-09-01") 
    profile_picture = models.ImageField(db_column="Zdjęcie profilowe",upload_to='pfps/',default='pfps/blank_user.png')
    
    def __str__(self):
        return self.user.username

# Create User Profile on User account registration
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, date_joined = instance.date_joined)
    else:
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.date_joined = instance.date_joined
        profile.save()
        
     