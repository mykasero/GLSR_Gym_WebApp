from django.db import models

# Create your models here.

class Booking(models.Model):
    users = models.CharField(db_column="Uzytkownicy",max_length=100)
    hours = models.DateTimeField(db_column="Godziny")
    #Hours + d/m/y auto added
    # pass
    
class Archive(models.Model):
    #Usernames
    #Hours + d/m/y auto added
    users = models.CharField(db_column="Uzytkownicy",max_length=100)
    hours = models.DateTimeField(db_column="Godziny")
    
    # pass
