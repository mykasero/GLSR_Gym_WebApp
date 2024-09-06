from django.db import models
import datetime
# Create your models here.
now = datetime.datetime.now()
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100, default="User")
    users_amount = models.IntegerField(db_column = "Ilosc osob", default=0)
    # start_hour + end_hour vs just start_hour TBD
    start_hour = models.TimeField(db_column= "Start" , default = str(now.hour) + ":" + str(now.minute))
    end_hour = models.TimeField(db_column = "Koniec", default = str(now.hour) + ":" + str(now.minute+1))
    current_day = models.DateTimeField(db_column = "Data", default = str(now.day) + "/" + str(now.month) + "/" + str(now.year))
    # pass
    
class Archive(models.Model):
    #Usernames
    #Hours + d/m/y auto added
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100, default="User")
    users_amount = models.IntegerField(db_column = "Ilosc osob", default=0)
    start_hour = models.TimeField(db_column= "Start" , default = str(now.hour) + ":" + str(now.minute))
    end_hour = models.TimeField(db_column = "Koniec", default = str(now.hour) + ":" + str(now.minute+1))
    current_day = models.DateTimeField(db_column = "Data", default = str(now.day) + "/" + str(now.month) + "/" + str(now.year))
    
    # pass
