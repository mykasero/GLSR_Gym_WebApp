from django.db import models
# import datetime
# Create your models here.
# now = datetime.datetime.now()
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100)
    users_amount = models.IntegerField(db_column = "Ilosc_osob")
    # start_hour + end_hour vs just start_hour TBD
    start_hour = models.TimeField(db_column= "Start")
    end_hour = models.TimeField(db_column = "Koniec")
    current_day = models.DateTimeField(db_column = "Data")
#     # pass
    
class Archive(models.Model):
#     #Usernames
#     #Hours + d/m/y auto added
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100)
    users_amount = models.IntegerField(db_column = "Ilosc osob")
    start_hour = models.TimeField(db_column= "Start")
    end_hour = models.TimeField(db_column = "Koniec")
    current_day = models.DateTimeField(db_column = "Data")
    
#     # pass
