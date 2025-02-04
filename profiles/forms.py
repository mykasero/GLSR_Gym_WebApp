from django import forms
import environ
from django.utils.translation import gettext as _
from .models import Profile
env = environ.Env()
environ.Env.read_env()

# email change form
class EmailForm(forms.Form):
    email = forms.EmailField(label="Adres email")
    access_code = forms.CharField(
        label="Kod dostępu:",
        help_text='Ten sam kod, który podajemy przy rejestracji',
        widget=forms.TextInput(attrs={
        'name':'access_code',
    }))
    

    def clean(self):
        email = self.cleaned_data.get('email')
        access_code = self.cleaned_data.get('access_code')

        
        if access_code not in [env("REGISTER_CODE"),env("ADMIN_REGISTER_CODE")]:
            self.add_error(None,   
                           forms.ValidationError(
                               _("Podano zły kod dostępu"),
                                code="invalid",
                                )
                           )
# profile picture change form       
class PfpForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

# Blank form, currently used for the rank info modal to display text    
class BlankForm(forms.Form):
    blank = forms.Textarea()
    
class PaymentForm(forms.Form):
    is_paid = forms.BooleanField( 
        label='Czy zapłacono?'
        )
    payment_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        help_text='Podaj date w formacie rok-miesiąc-dzień np. 2025-02-04',
        label = 'Data zapłacenia',
        )