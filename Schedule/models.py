from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
# Current bookings model
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100, help_text="Podana nazwa musi być nazwą zarejestrowanego użytkownika")
    users_amount = models.IntegerField(db_column = "Ilosc_osob",help_text="Podaj jako numer")
    start_hour = models.TimeField(db_column= "Start", help_text = "Podaj godzine w formacie np.: 12:20, lub zacznij podawać numery i wybierz odpowiadający ci z listy domyślnych wyborów (na tel nad klawiaturą)")
    end_hour = models.TimeField(db_column = "Koniec", help_text = "Ta godzina moze byc 'na oko', format taki sam jak powyżej")
    current_day = models.DateField(db_column = "Data", help_text = "Wybierz dzień" )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='created_by', blank = True, null = True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(users_amount__gt=0),
                name='booking_users_amount_gt_0'
            ),
        ]
    
    def clean(self):
        if self.users_amount <= 0:
            raise ValidationError('Nalezy podac liczbe wieksza od 0')
        
# Bookings archive model
class Archive(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.CharField(db_column="Uzytkownicy",max_length=100)
    users_amount = models.IntegerField(db_column = "Ilosc_osob")
    start_hour = models.TimeField(db_column= "Start")
    end_hour = models.TimeField(db_column = "Koniec")
    current_day = models.DateField(db_column = "Data")
    
    class Meta:
        ordering = ["-current_day"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(users_amount__gt=0),
                name='archive_users_amount_gt_0'
            ),
        ]
    
    def clean(self):
        if self.users_amount <= 0:
            raise ValidationError('Nalezy podac liczbe wieksza od 0')
    
# Key stash keycodes model
class Keycodes(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(db_column="Kod_Skrytki", max_length=4, help_text="Cztery cyfry 0-9")
    code_date = models.DateField(db_column="Data dodania")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition = models.Q(code__regex=r'^\d{4}$'),
                name = 'code_must_be_4_digits',
            ),
        ]

    def clean(self):
        if not self.code.isnumeric():
            raise ValidationError('Podany kod nie składa się tylko z liczb')
        if len(self.code) < 4:
            raise ValidationError('Podany kod jest za krótki')
        
# Bug Reports model  
class BugReports(models.Model):
    id = models.AutoField(primary_key=True)
    report_text = models.CharField(db_column="Opis bledu", max_length=1000, help_text="Opisz problem, jakie kroki zrobiles zanim sie pojawil")
    report_date = models.DateField(db_column="Data zgloszenia", help_text="Data dnia wystapienia problemu")
    
class CleaningSchedule(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.TextField(db_column="Nazwa_Użytkownika")
    period_start = models.DateField(db_column="Okres obowiązywania start")
    period_end = models.DateField(db_column="Okres obowiązywania koniec")