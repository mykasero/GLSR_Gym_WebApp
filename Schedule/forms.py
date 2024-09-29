from django import forms
from .models import Booking, Keycodes, BugReports
from django.contrib.auth import login, authenticate, get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, SetPasswordMixin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import environ

env = environ.Env()
environ.Env.read_env()

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
        
        self.fields['password1'].help_text = mark_safe('<ul><li>Nie podawaj swojego prawdziwego hasła.</li><li>Minimum 8 znaków.</li><li>Nie może być podobne do loginu.</li><li>Nie może być całkowicie złożone z cyfr.</li></ul>')
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
    
    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        access_code = cleaned_data.get('access_code')
        
        if password1 != password2:
            self.add_error(None,forms.ValidationError(_("Hasła nie są takie same"),
                                  code="invalid",
                                  ))
        
        if password1 == "" or password2 == "" or (password1 == "" and password2 == ""):
            self.add_error(None,forms.ValidationError(_("Pola haseł nie mogą być puste"),
                                  code="invalid",
                                  ))
        if len(password1) < 8:
            self.add_error(None,forms.ValidationError(_("Hasło za krótkie, minimalna długość 8 znaków"),
                                  code="invalid",
                                  ))
        
        if username is None:
            self.add_error(None,   
                           forms.ValidationError(
                               _("Użytkownik o takiej nazwie już istnieje"),
                                code="invalid",
                                )
                           )

        elif len(username) > 50:
            self.add_error(None,forms.ValidationError(_("Nazwa za długa, maksymalna długość - 50 znaków"),
                                  code="invalid",
                                  ))
        
        if access_code not in [env("REGISTER_CODE"),env("ADMIN_REGISTER_CODE")]:
            self.add_error(None,   
                           forms.ValidationError(
                               _("Podano zły kod dostępu"),
                                code="invalid",
                                )
                           )
        
        if password1.isdigit():
            self.add_error(None,   
                           forms.ValidationError(
                               _("Hasło nie może być złożone z samych cyfr"),
                                code="invalid",
                                )
                           )
        
        return cleaned_data
    
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
    
    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('users')
        start = cleaned_data.get('start_hour')
        end = cleaned_data.get('end_hour')
        amount = cleaned_data.get('users_amount')
        
        # Booking Validations
        
        # If username is not registered throw error
        User = get_user_model()
        users_list = User.objects.values('username')
        if username not in [value['username'] for value in list(users_list)]:
             self.add_error(None,forms.ValidationError(_("Podana nazwa (%(username)s) nie jest na liście zarejestrowanych użytkowników"),
                                  code="invalid",
                                  params = {'username' : username}))
        
        # If end hour is earlier than start hour throw error    
        if end < start:
            self.add_error(None,forms.ValidationError(_("Godzina końca %(end)s nie może być mniejsza niż godzina startu %(start)s"),
                                  code="invalid",
                                  params = {'end' : end, 'start' : start}))
        
        # If amount of user in booking are more than 5 throw error    
        if amount > 5:
            self.add_error(None,forms.ValidationError(_("Przekroczono maksymalna ilosc osob (%(amount)s) w rezerwacji"),
                                  code="invalid",
                                  params = {'amount' : amount}))   
        
        
        return cleaned_data
    
    
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