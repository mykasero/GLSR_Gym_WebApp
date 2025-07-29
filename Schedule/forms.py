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
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
env = environ.Env()
environ.Env.read_env()

def dates1():
    DATES1 = [
        datetime.date.today() + datetime.timedelta(days=i) for i in range(0,3)
        ]
    DAYS1 = ["Dzisiaj", "Jutro", "Pojutrze"]
    DATES_SELECT1 = [(date, day) for date, day in zip(DATES1, DAYS1)]
    
    return DATES_SELECT1

def dates_bugreport():
    # Create a list of dates starting from 3days ago until today included)    
    DATES_BUGREPORT = [
        datetime.date.today() + datetime.timedelta(days=i) for i in range(-3,1)
        ]
    # List of days names
    DAYS_BUGREPORT = ["3 dni temu","2 dni temu", "Wczoraj", "Dzisiaj"]
    # Creating a list of tuples for SELECT widget
    DATES_SELECT_BUGREPORT = [(date, day) for date, day in zip(
        DATES_BUGREPORT, DAYS_BUGREPORT
        )]

    return DATES_SELECT_BUGREPORT


# Get dates for 3 days starting from today
# DATES1 = [datetime.date.today() + datetime.timedelta(days=i) for i in range(0,3)]
# Names for today, tomorrow, 2 days after 
# DAYS1 = ["Dzisiaj", "Jutro", "Pojutrze"]
# Zip the dates and day names for type friendly to SELECT widget
# DATES_SELECT1 = [(date, day) for date, day in zip(DATES1, DAYS1)]

TODAY = [(datetime.date.today(),"Dzisiaj")]

def hour_list():
    HOUR_LIST = []
    # Create a list of hours for auto complete in booking
    for hour in range(0,24):
        for minute in range(0,60,15):
                if hour == 0:
                    if minute == 0:
                        HOUR_LIST.append("00:00")
                    else:
                        HOUR_LIST.append("00:"+str(minute))
                
                elif hour < 10:
                    if minute==0:
                        HOUR_LIST.append("0"+str(hour)+":00") 
                    else:
                        HOUR_LIST.append("0"+str(hour)+":"+str(minute))
                else:
                    if minute==0:    
                        HOUR_LIST.append(str(hour)+":00")
                    else:                     
                        HOUR_LIST.append(str(hour)+":"+str(minute))
    # Create a list of tuples for SELECT widget
    for i in range(len(HOUR_LIST)):
        HOUR_LIST[i] = (HOUR_LIST[i],HOUR_LIST[i])
    
    return HOUR_LIST



# Keycodes model form
class KeycodeForm(forms.ModelForm):
    # Get todays datetime
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

# Login Form
class LoginForm(forms.Form):
    login = forms.CharField(label = '', 
                            max_length=50, 
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Login'}
                                ))
    haslo = forms.CharField(label = '', 
                            widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Haslo'}
                                ), 
                            max_length=40)
    
# Register form
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        # override Djangos default label
        self.fields['password1'].label = mark_safe('<strong>Hasło</strong>')
        self.fields['password2'].label = mark_safe(
            '<strong>Potwierdź hasło</strong>'
            )
        # override Djangos default helptext
        self.fields['password1'].help_text = mark_safe(
            '<ul><li>Nie podawaj swojego prawdziwego hasła.\
            </li><li>Minimum 8 znaków.</li>\
            <li>Nie może być podobne do loginu.</li>\
            <li>Nie może być całkowicie złożone z cyfr.</li></ul>'
            )
        self.fields['password2'].help_text = ' '
    
    # Add an access_code field for register form
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
            'username' : 'Max długość 50 znaków. Dozwolone litery, \
                cyfry i symbole @/./+/-/_',
        }
    
    # Create validation checks
    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        access_code = cleaned_data.get('access_code')
        
        # If passwords don't match throw error
        if password1 != password2:
            self.add_error(None,forms.ValidationError(
                _("Hasła nie są takie same"),
                code="invalid",
            ))
        # If any of the passwords ( or both ) are empty, throw error
        if password1 == "" or \
            password2 == "" or \
            (password1 == "" and password2 == ""):
            self.add_error(None,forms.ValidationError(
                _("Pola haseł nie mogą być puste"),
                code="invalid",
            ))
        # If password shorter than 8 chars, throw error
        if len(password1) < 8:
            self.add_error(None,forms.ValidationError(
                _("Hasło za krótkie, minimalna długość 8 znaków"),
                code="invalid",
            ))
        
        # If username is empty, throw error
        if username is None:
            self.add_error(None,   
                           forms.ValidationError(
                               _("Użytkownik o takiej nazwie już istnieje"),
                                code="invalid",
                                )
                           )
        # If username is longer than 50 chars, throw error
        elif len(username) > 50:
            self.add_error(None,forms.ValidationError(
                _("Nazwa za długa, maksymalna długość - 50 znaków"),
                code="invalid",
            ))
        
        # If access_code is wrong, throw error
        if access_code not in [env("REGISTER_CODE"),env("ADMIN_REGISTER_CODE")]:
            self.add_error(None,   
                           forms.ValidationError(
                               _("Podano zły kod dostępu"),
                                code="invalid",
                                )
                           )
        # If password is only numeric, throw error
        if password1.isdigit():
            self.add_error(None,   
                           forms.ValidationError(
                               _("Hasło nie może być złożone z samych cyfr"),
                                code="invalid",
                                )
                           )
        
        return cleaned_data

# Bookings model form 
class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args,**kwargs)
        self.fields['start_hour'].widget = forms.Select(choices=hour_list())
        self.fields['end_hour'].widget = forms.Select(choices=hour_list())
        self.fields['current_day'].widget = forms.Select(
            choices=dates1(),
            attrs={'class':"form-select"}
        )
    class Meta:
        model = Booking
        fields = ["users","users_amount","start_hour","end_hour","current_day"]
        # widgets = {
        #     'current_day' : forms.Select(choices=dates1())
        # }
        labels = {
            'users' : mark_safe('<strong>Nazwa</strong>'),
            'users_amount' : mark_safe('<strong>Ile osób</strong>'),
            'start_hour' : mark_safe('<strong>Godzina Start</strong>'),
            'end_hour' : mark_safe('<strong>Godzina Koniec</strong>'),
            'current_day' : mark_safe('<strong>Dzień</strong>'),
        }
    
    # Create validation checks
    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('users')
        start = cleaned_data.get('start_hour')
        end = cleaned_data.get('end_hour')
        amount = cleaned_data.get('users_amount')
        
       
        
        # If username is not found in registered usernames throw error
        User = get_user_model()
        users_list = User.objects.values('username')
        if username not in [value['username'] for value in list(users_list)]:
             self.add_error(None,forms.ValidationError(
                 _("Podana nazwa (%(username)s) nie jest na liście\
                     zarejestrowanych użytkowników"),
                code="invalid",
                params = {'username' : username})
                )
        
        #Look into form taking only hour as well with hour:minute
        
        # If start or end is in wrong format (only hour for example) 
        # throw this error
        # !!!This is a temporary solution!!!
        if start is None or end is None:
            self.add_error(None,forms.ValidationError(
                _("Podano zły format godziny."),
                code="invalid",
            ))
        # If end hour is earlier than start hour throw error    
        elif end < start:
            self.add_error(None,forms.ValidationError(
                _("Godzina końca %(end)s nie może być mniejsza \
                    niż godzina startu %(start)s"),
                code="invalid",
                params = {'end' : end, 'start' : start})
            )
        
        # If amount of users in booking are more than 5 throw error    
        if amount > 5:
            self.add_error(None,forms.ValidationError(
                _("Przekroczono maksymalna ilosc osob \
                    (%(amount)s) w rezerwacji"),
                code="invalid",
                params = {'amount' : amount})
            )   
        
        
        
        return cleaned_data
    

class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReports
        fields = ["report_date","report_text"]
        widgets = {
            'report_date' : forms.Select(choices=dates_bugreport()),
            'report_text' : forms.Textarea(attrs={
                'class' : 'form-group form-control',
                'rows':'3','style':'height: 200px'}) 
        }



class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args,**kwargs)
        
    username = forms.CharField(label="Nazwa Użytkownika:",
                               widget=forms.TextInput(attrs={
                                    'placeholder':'koxu123',
                                    'name':'username',
                                    })
                                )
    
    email = forms.EmailField(label="Email:",
        help_text='Adres email na który przyjdzie link do zmiany hasła',
        widget=forms.EmailInput(attrs={
        'placeholder':'koxu123@gmail.com',
        'type':'email',
        'name':'email',
    }))
    
    access_code = forms.CharField(
        label="Kod dostępu:",
        help_text='Ten sam kod, który podajemy przy rejestracji',
        widget=forms.TextInput(attrs={
        'name':'access_code',
    }))
    
    def get_users(self, username):
        User = get_user_model()
        return User.objects.filter(username=username)
    
    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        access_code = self.cleaned_data.get('access_code')
        users = self.get_users(username)

        if not users.exists():
            self.add_error(None,forms.ValidationError(
                _("Podana nazwa (%(username)s) nie jest na\
                    liście zarejestrowanych użytkowników"),
                code="invalid",
                params = {'username' : username})
            )
            
        
        if access_code not in [env("REGISTER_CODE"),env("ADMIN_REGISTER_CODE")]:
            self.add_error(None,   
                           forms.ValidationError(
                               _("Podano zły kod dostępu"),
                                code="invalid",
                                )
                           )  
        
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args,**kwargs)
    
    new_password1 = forms.CharField(
        label=_("Nowe hasło"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=mark_safe(
            '<ul><li>Nie podawaj swojego prawdziwego hasła.</li>\
            <li>Minimum 8 znaków.</li>\
            <li>Nie może być podobne do loginu.</li>\
            <li>Nie może być całkowicie złożone z cyfr.</li></ul>'
        ),
    )
    
    new_password2 = forms.CharField(
        label=_("Potwierdź nowe hasło"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=mark_safe('Powtórz hasło'),
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        
        # If passwords don't match throw error
        if new_password1 != new_password2:
            self.add_error(None,forms.ValidationError(
                _("Hasła nie są takie same"),
                code="invalid",
                )
            )
        # If any of the passwords ( or both ) are empty, throw error
        if new_password1 == "" or \
            new_password2 == "" or \
            (new_password1 == "" and new_password2 == ""):
            self.add_error(None,forms.ValidationError(
                _("Pola haseł nie mogą być puste"),
                code="invalid",
                )
            )
        # If password shorter than 8 chars, throw error
        if len(new_password1) < 8:
            self.add_error(None,forms.ValidationError(
                _("Hasło za krótkie, minimalna długość 8 znaków"),
                code="invalid",
                )
            )

        # If password is only numeric, throw error
        if new_password1.isdigit():
            self.add_error(None,   
                           forms.ValidationError(
                               _("Hasło nie może być złożone z samych cyfr"),
                                code="invalid",
                                )
                           )
        
        return cleaned_data