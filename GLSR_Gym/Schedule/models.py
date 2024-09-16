from django.db import models

# Create your models here.


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100)
    users_amount = models.IntegerField(db_column = "Ilosc_osob")
    # start_hour + end_hour vs just start_hour TBD
    start_hour = models.TimeField(db_column= "Start")
    end_hour = models.TimeField(db_column = "Koniec", help_text= "Ta godzina moze byc 'na oko'")
    current_day = models.DateField(db_column = "Data", help_text="Wybierz dzien" )
#     # pass
    
class Archive(models.Model):
#     #Usernames
#     #Hours + d/m/y auto added
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100)
    users_amount = models.IntegerField(db_column = "Ilosc osob")
    start_hour = models.TimeField(db_column= "Start")
    end_hour = models.TimeField(db_column = "Koniec")
    current_day = models.DateField(db_column = "Data")
    
#     # pass
class Keycodes(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(db_column="Kod_Skrytki", max_length=4)
    code_date = models.DateField(db_column="Data dodania")