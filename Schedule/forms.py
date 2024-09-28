from django import forms
from .models import Booking, Keycodes, BugReports
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, SetPasswordMixin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import datetime
DATES1 = [datetime.date.today() + datetime.timedelta(days=i) for i in range(0,3)]
DAYS1 = ["Dzisiaj", "Jutro", "Pojutrze"]

DATES_SELECT1 = [(date, day) for date, day in zip(DATES1, DAYS1)]
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
    login = forms.CharField(label = '', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    haslo = forms.CharField(label = '', widget=forms.PasswordInput(attrs={'placeholder': 'Haslo'}), max_length=40)
    
        
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password1'].label = mark_safe('<strong>Hasło</strong>')
        self.fields['password2'].label = mark_safe('<strong>Potwierdź hasło</strong>')
        
        self.fields['password1'].help_text = '<ul><li>Nie podawaj swojego prawdziwego hasła.</li><li>Minimum 8 znaków.</li><li>Nie może być podobne do loginu.</li><li>Nie może być całkowicie złożone z cyfr.</li></ul>'
        self.fields['password2'].help_text = ' '
    
    access_code = forms.CharField(
        label=mark_safe("<strong>Kod Dostepu</strong>"),
        help_text=" ",
    )
    usable_password = None
    class Meta:
        model = User
        fields = ['username','password1','password2','access_code']

        labels={
            'username' : mark_safe('<strong>Nazwa użytkownika</strong>'),
        }
        help_texts= {
            'username' : 'Max długość 50 znaków. Dozwolone litery, cyfry i symbole @/./+/-/_',
        }
        
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["users","users_amount","start_hour","end_hour","current_day"]
        widgets = {
            'current_day' : forms.Select(choices=DATES_SELECT1)
        }
        labels = {
            'users' : mark_safe('<strong>Nazwa</strong>'),
            'users_amount' : mark_safe('<strong>Ile osób</strong>'),
            'start_hour' : mark_safe('<strong>Godzina Start</strong>'),
            'end_hour' : mark_safe('<strong>Godzina Koniec</strong>'),
            'current_day' : mark_safe('<strong>Dzień</strong>'),
        }
    
    
DATES_BUGREPORT = [datetime.date.today() + datetime.timedelta(days=i) for i in range(-3,1)]
DAYS_BUGREPORT = ["3 dni temu","2 dni temu", "Wczoraj", "Dzisiaj"]
DATES_SELECT_BUGREPORT = [(date, day) for date, day in zip(DATES_BUGREPORT, DAYS_BUGREPORT)]

class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReports
        fields = ["report_date","report_text"]
        widgets = {
            'report_date' : forms.Select(choices=DATES_SELECT_BUGREPORT),
            'report_text' : forms.Textarea(attrs={'class' : 'form-group form-control','rows':'3','style':'height: 200px'}) 
        }