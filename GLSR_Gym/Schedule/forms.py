from django import forms
from Schedule.models import Booking
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, SetPasswordMixin
from django.contrib.auth.models import User


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
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["users","users_amount","start_hour","end_hour","current_day"]