from django import forms
from Schedule.models import Booking



class LoginForm(forms.Form):
    login = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    haslo = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Haslo'}), max_length=40)
    
        
