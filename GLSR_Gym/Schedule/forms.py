from django import forms
from Schedule.models import Booking

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    login = forms.CharField(label = '', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    haslo = forms.CharField(label = '', widget=forms.PasswordInput(attrs={'placeholder': 'Haslo'}), max_length=40)
    
        
class RegisterForm(UserCreationForm):
    access_code = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username','password1','password2','access_code']