from django import forms
from .models import Booking, Keycodes
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, SetPasswordMixin
from django.contrib.auth.models import User

import datetime
DATES_SELECT = [datetime.date.today() + datetime.timedelta(days=i) for i in range(-1,3)]
DAYS = ["Wczoraj","Dzisiaj", "Jutro", "Pojutrze"]

DATES_SELECT1 = [(date, day) for date, day in zip(DATES_SELECT, DAYS)]
TODAY = [(datetime.date.today(),"Dzisiaj")]

class KeycodeForm(forms.ModelForm):
    code_date = datetime.date.today()
    class Meta:
        model = Keycodes
        fields = ["code","code_date"]
        widgets = {
            'code_date' : forms.Select(choices=TODAY)
        }
        labels = {
            "code" : "Kod do skrytki",
            "code_date" : "Data dodania kodu",
        }

class LoginForm(forms.Form):
    login = forms.CharField(label = '', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    haslo = forms.CharField(label = '', widget=forms.PasswordInput(attrs={'placeholder': 'Haslo'}), max_length=40)
    
        
class RegisterForm(UserCreationForm):
    access_code = forms.CharField(
        label="Kod Dostepu:",
        help_text=" ",
    )
    usable_password = None
    class Meta:
        model = User
        fields = ['username','password1','password2','access_code']
        
        labels={
            'username' : 'Nazwa użytkownika',
            'password1' : 'Hasło',
            'password2' : 'Potwierdź hasło',
        }
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["users","users_amount","start_hour","end_hour","current_day"]
        widgets = {
            'current_day' : forms.Select(choices=DATES_SELECT1)
        }
        labels = {
            'users' : 'Imie:',
            'users_amount' : 'Ile osob:',
            'start_hour' : 'Godzina startu:',
            'end_hour' : 'Godzina konca:',
            'current_day' : 'Dzien',
        }