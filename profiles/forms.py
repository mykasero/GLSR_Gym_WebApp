from django import forms
import environ

env = environ.Env()
environ.Env.read_env()

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