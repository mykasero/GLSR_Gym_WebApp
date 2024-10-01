from django.db import models

# Create your models here.


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100, help_text="Podana nazwa musi być nazwą zarejestrowanego użytkownika")
    users_amount = models.IntegerField(db_column = "Ilosc_osob",help_text="Podaj jako numer")
    start_hour = models.TimeField(db_column= "Start", help_text = "Przykładowy format: 12:20")
    end_hour = models.TimeField(db_column = "Koniec", help_text = "Ta godzina moze byc 'na oko', format taki sam jak powyżej")
    current_day = models.DateField(db_column = "Data", help_text = "Wybierz dzień" )
    
class Archive(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100)
    users_amount = models.IntegerField(db_column = "Ilosc_osob")
    start_hour = models.TimeField(db_column= "Start")
    end_hour = models.TimeField(db_column = "Koniec")
    current_day = models.DateField(db_column = "Data")
    

class Keycodes(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(db_column="Kod_Skrytki", max_length=4, help_text="Cztery cyfry 0-9")
    code_date = models.DateField(db_column="Data dodania")
    
class BugReports(models.Model):
    id = models.AutoField(primary_key=True)
    report_text = models.CharField(db_column="Opis bledu", max_length=1000, help_text="Opisz problem, jakie kroki zrobiles zanim sie pojawil")
    report_date = models.DateField(db_column="Data zgloszenia", help_text="Data dnia wystapienia problemu")